## Aloha Robotic Arm 

Static Aloha vs Mobile Aloha 

Aloha Robotic arm environment,  

Notedly it has 16 DoF (degrees of freedom)

Waist (-pi to pi) , shoulder, elbow, forearm ( -pi to pi) , wrist , wrist rotation (-pi to pi) , finger-1 , finger-2 and then same repeated for in the other arm. 


Actual : 6 for arms + 2 for grippers => 8 values 


but for continuity, 6 arms + 1 for gripper 
Gripper : 0 closed , 1 open so 0.5 means its like a number line , 
`0 to 1, 0 to 0.5 for one finger, then 0.5 to 1 for other finger` 
This is how this works in the dataset 

