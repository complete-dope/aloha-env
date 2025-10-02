## Aloha robot 

This has 2 Robot arms that are left and right and each has 8 dof 

The camera used in simulation has 3 properties: 

elevation : This is the angle from the zenith to the nadir .. from top point to the bottom point  
distance 
azimuth : This is east to west like rotating around a table 
center : its the one where the camera points at [x,y,z] it has x, y, z coordinates 

* The object is placed somewhere on the y-axis and we have x in the same plane as board so basically board is in the x-y plane and zenith is in the z-axis



## adding more camera to the robot 
You add cameras to the objects in the XML file itself in the world-body

```
<worldbody>
  <body name="cameramover" mocap="true" pos="0 0 1">
    <camera name="mycamera" pos="0  -2  1"  euler="30 0 0"/>
  </body>
  ...
</worldbody>
```

here above we created a camera but didnt told its type , possible types are : 
```
mjCAMERA_FREE
mjCAMERA_TRACKING 
mjCAMERA_FIXED
mjCAMERA_USER 
```

Use those cameras as, mjvCamera for active camera
3 types of cameras: 
CAMERA_FREE , CAMERA_TRACKING, CAMERA_FIXED, CAMERA_USER

Once you define all these relevant attributes, create an object for mjvScene to be able to use that in scene 


Added the wrist already had that camera's ... I just needed to activate those  

Policy is trained in here :  https://huggingface.co/lerobot/act_aloha_sim_insertion_human 



You can use this policy in the hugging face 

