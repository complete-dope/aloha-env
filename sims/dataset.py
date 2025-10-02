# view the actions from the dataset

def dataset_creation():
  from datasets import load_dataset

  # Login using e.g. `huggingface-cli login` to access this dataset
  ds = load_dataset("lerobot/aloha_sim_transfer_cube_human")

  print('sample dataset is : ', ds['train'][0])

  sample = ds['train'][0]

  def convert_to_dof_16(action):
      assert len(action) == 14 , 'This is the expected shape of the dataset '

      left_grips = action[0:6]
      right_grips = action[7:13]


      left_gripper = action[6] 

      min_left_left_gripper = 0.021 
      high_left_left_gripper = 0.057

      min_left_right_gripper = -0.021
      high_left_right_gripper = -0.057

      left_fing_1 = left_gripper * (high_left_left_gripper - min_left_left_gripper) + min_left_left_gripper
      left_fing_2 = left_gripper * (high_left_right_gripper - min_left_right_gripper) + min_left_right_gripper

      # right side gripper !! 
      right_gripper= action[13] # 0.18998171389102936

      min_right_left_gripper = 0.021
      high_right_left_gripper =  0.057

      min_right_right_gripper = -0.021
      high_right_right_gripper = -0.057

      right_fing_1 = right_gripper * (high_right_left_gripper - min_right_left_gripper) + min_right_left_gripper
      right_fing_2 = right_gripper * (high_right_right_gripper - min_right_right_gripper) + min_right_right_gripper

      return left_grips + [left_fing_1, left_fing_2] + right_grips + [right_fing_1, right_fing_2]

  def episode_collection(ds):
    df = ds['train']
    action_set = []
    episode = None
    for idx in range(len(df)):
      sample = df[idx]
      cur_episode = sample['episode_index']
      if episode is not None and episode == cur_episode:
        action_set.append(sample['action'])
      elif episode is None:
        episode = cur_episode
        action_set.append(sample['action'])
      else:
        break
      
    df_16 = []
    for action in action_set:
      df_16.append(convert_to_dof_16(action))
      
    return df_16

''' 
  -0.30000001192092896,
  0.0,
  0.0],
 'action': [-0.013805827125906944,
  -0.9295923709869385,
  1.179631233215332,
  -0.003067961661145091,
  -0.3298058807849884,
  -0.0015339808305725455,
  0.1636791080236435,
  0.010737866163253784,
  -0.9295923709869385,
  1.2026410102844238,
  -0.0015339808305725455,
  -0.3190680146217346,
  0.015339808538556099,
  0.18998171389102936],
 'episode_index': 0,

'''