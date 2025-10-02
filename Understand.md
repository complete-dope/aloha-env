https://github.com/huggingface/gym-aloha

This is the one where the huggingface guys tried out there trained model  

Env : Where we define the robot's env using the .xml file   

Simulation : the one where define the simulation for the robot its action space 

Scene : 3d scene , robots current environment screenshot, the snapshot of current state 

Context : Its the one used for rendering using the GPU , machines

Render: This is to show the it on the screen ( only scene can be rendered )

## Process of using mujoco Simple

First we load a model from the xml file, then we create a scene out of it 
Then we load the simulation data for our model

then everything defined in XML doesnt get auto used , we have to explicitly use it
define the object, fix in some attribute values 

Define a single scene and that only we can reuse multiple times 

then render it to of-screen or on-screen using the mjv_render() takes in :   
`3 args : (where, what, who-will-do) -> (viewport, scene, context)`




