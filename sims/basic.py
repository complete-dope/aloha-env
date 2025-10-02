# THIS IS BASED ON IMITATION LEARNING 

# basic_gui.py  -- for mujoco python bindings (v2.1+ / 2.3+)
import mujoco
from mujoco.glfw import glfw
import numpy as np
import sys
import time
import imageio

XML = "/Users/mohitdulani/Desktop/personal/robotics/sims/assets/bimanual_viperx_transfer_cube.xml"

# Model : The environment where the robot interacts lives with and working
model = mujoco.MjModel.from_xml_path(XML)

# Simulation : state of the robot, joint velocities, joint positions , angle  
data  = mujoco.MjData(model)

# GLFW + OpenGL window => Graphic + Input handler ( window creation , openGL )
if not glfw.init():
    raise RuntimeError("glfw.init failed")


# left wrist camera
left_wrist_cam = mujoco.MjvCamera()
left_wrist_cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
left_wrist_cam.fixedcamid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "left_wrist") # get id of object and return -1
if left_wrist_cam.fixedcamid == -1:
    print('The name was not found for the mentioned object type')
left_wrist_scene = mujoco.MjvScene(model, maxgeom=2000)

# right wrist camera
right_wrist_cam = mujoco.MjvCamera()
right_wrist_cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
right_wrist_cam.fixedcamid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "right_wrist")
right_wrist_scene = mujoco.MjvScene(model, maxgeom=2000) # This creates an object for MjvScene and is a key component for visualising mujoco model 


window = glfw.create_window(1280, 720, "MuJoCo GUI", None, None)
glfw.make_context_current(window)

# Abstract scene + render context (correct objects)
scene   = mujoco.MjvScene(model, maxgeom=2000)
cam     = mujoco.MjvCamera()     # you can change cam.azimuth/distance/elevation/lookat
pert    = mujoco.MjvPerturb()    # unused unless you enable mouse perturb
opt     = mujoco.MjvOption()     # default rendering options
context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150)

# set a sensible camera view
cam.lookat[:] = np.array([0.2, 0.0, 0.1])   # center on your workspace
cam.distance  = 1.2 
cam.azimuth   = 90.0 # --> changing azimuth means the camera is moving around the entire scene like around a table ( from east to west )  
cam.elevation = -30.0 # --> its also the camera moving from the zenith to the nadir .. 

init = None  # lazy init
def random_actions(idx: int):
    global init
    ctrl = np.zeros(model.nu)

    # target final state
    final = np.array([
        -0.094, -0.157, 0.764, 2.23, -0.965, -1.98,
        0.021, -0.023, 0.0004, -0.00679, 0.831,
        0.00216, -0.00499, -0.00877, -0.027, 0.0257
    ])

    # initialize only once
    if init is None:
        init = ctrl.copy()

    # period = 400 steps (200 forward, 200 back)
    period = 400
    t = idx % period

    # normalize progress [0,1]
    if t < 200:  # going forward
        alpha = t / 200
    else:        # coming back
        alpha = 1 - (t - 200) / 200

    # linear interpolation
    new_state = init * (1 - alpha) + final * alpha

    ctrl[:] = new_state
    return ctrl

try:
    last = time.time()
    idx = 0
    while not glfw.window_should_close(window):
        # step physics (you may call mj_step1/mj_step2 for custom substepping)
        rand_action_data = random_actions(idx)
        # print('random action data', len(rand_action_data)) # 16 action in total that gets rendered !

        data.ctrl[:] = rand_action_data
        mujoco.mj_step(model, data) # here the new data state gets updated 

        # IMPORTANT: correct order and argument types for mjv_updateScene
        mujoco.mjv_updateScene(model, data, opt, pert, cam, mujoco.mjtCatBit.mjCAT_ALL, scene) # updates entire scene 

        # render main camera
        viewport = mujoco.MjrRect(0, 0, *glfw.get_framebuffer_size(window))
        mujoco.mjr_render(viewport, scene, context)

        # render wrist cameras
        width, height = glfw.get_framebuffer_size(window)
        wrist_width, wrist_height = 320, 240
        
        # left wrist
        left_wrist_viewport = mujoco.MjrRect(width - wrist_width, 0, wrist_width, wrist_height)
        mujoco.mjv_updateScene(model, data, opt, pert, left_wrist_cam, mujoco.mjtCatBit.mjCAT_ALL, left_wrist_scene)
        mujoco.mjr_render(left_wrist_viewport, left_wrist_scene, context)
        mujoco.mjr_text(mujoco.mjtFont.mjFONT_NORMAL, "Left Wrist", context, width - wrist_width + 5, 5, 0, 0, 0)

        # right wrist
        right_wrist_viewport = mujoco.MjrRect(width - wrist_width, wrist_height, wrist_width, wrist_height)
        mujoco.mjv_updateScene(model, data, opt, pert, right_wrist_cam, mujoco.mjtCatBit.mjCAT_ALL, right_wrist_scene)
        mujoco.mjr_render(right_wrist_viewport, right_wrist_scene, context) #renders a scene
        mujoco.mjr_text(mujoco.mjtFont.mjFONT_NORMAL, "Right Wrist", context, width - wrist_width + 5, wrist_height + 5, 0, 0, 0)

        # glfw housekeeping
        glfw.swap_buffers(window) # to avoid the strokes to the user, rather the computatioon is done behidnd this just swaps it out .. 
        glfw.poll_events()

        # optional: print/sync at ~60Hz
        now = time.time()
        if now - last >= 1.0/10.0:
            print("-- ->>> qpos[:8]", np.round(data.qpos[:8],4))
            last = now

        idx +=1

        if idx %100 ==0:
            # save the image from the cameras
            mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_OFFSCREEN, context) # its says from now on dont render this on-screen
            # create a new viewport for the offscreen rendering
            offscreen_viewport = mujoco.MjrRect(0, 0, wrist_width, wrist_height)
            
            # It's good practice to update scene right before render
            mujoco.mjv_updateScene(model, data, opt, pert, left_wrist_cam, mujoco.mjtCatBit.mjCAT_ALL, left_wrist_scene)
            mujoco.mjr_render(offscreen_viewport, left_wrist_scene, context)

            rgb = np.zeros((wrist_height, wrist_width, 3), dtype=np.uint8)
            mujoco.mjr_readPixels(rgb, None, offscreen_viewport, context)
            rgb = np.flipud(rgb)   # fix upside-down
            # store this

            print(rgb.shape)
            imageio.imwrite("camera_feed.png", rgb)

            # unset it also 
            mujoco.mjr_setBuffer(mujoco.mjtFramebuffer.mjFB_WINDOW, context) # its says from now on dont render this on-screen



finally:
    # cleanup
    # mujoco.mjr_freeContext(context) # deprecated

    ## TODO : check if not a black image, if black image then code didnt worked out 
     

    glfw.terminate()