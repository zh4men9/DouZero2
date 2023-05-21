# DouZero_ADP vs Random
# DouZero_ADP vs SL
# DouZero_ADP vs rlcard

# DouZero_WP vs Random
# DouZero_WP vs SL
# DouZero_WP vs rlcard

# DouZero_ADP的checkpoints保存在./douzero_checkpoints/douzero
# DouZero_WP的checkpoints保存在./douzero_checkpoints_wp/douzero

# DouZero模型都加载landlord_weights
# SL加载landlord_up和landlord_down

# DouZero正在训练，有很多的checkpoints，需要都加载进来去evaluate
# 对于DouZero_WP vs Random：python evaluate.py --landlord {DouZero_checkpoints_path} --landlord_up random --landlord_down random
# 对于DouZero_ADP vs SL：python evaluate.py --landlord {DouZero_checkpoints_path} --landlord_up baselines/sl/landlord_up.ckpt --landlord_down baselines/sl/landlord_down.ckpt
# 对于DouZero_ADP vs rlcard：python evaluate.py --landlord {DouZero_checkpoints_path} --landlord_up rlcard --landlord_down rlcard

# 由于evaluate一次需要很久时间，所以需要将每次evaluate的结果保存在evaluate_result文件夹下，每次执行这个文件的时候，都需要判断某个checkpoints是否已经evaluate了
import os
import subprocess

def run_evaluate(landlord_weights, landlord_up, landlord_down, save_dir):
    if ('wp' in landlord_weights):
        model_type = 'WP'
    else:
        model_type = 'ADP'
        
    if ('sl' in landlord_up):
        name_parts = [model_type, 'SL']
    else:
        name_parts = [model_type, landlord_up]
        
    checkpoint_files = os.listdir(landlord_weights)
    cnt = 0
    for checkpoint_file in checkpoint_files:
        # only consider landlord checkpoints
        if 'landlord' in checkpoint_file and 'landlord_up' not in checkpoint_file and 'landlord_down' not in checkpoint_file:
            if (cnt >= 2):
                return
            else:
                cnt += 1
            # Create a name for the result directory
            
            result_dir_name = '_'.join(name_parts)
            result_dir = os.path.join(save_dir, result_dir_name)
            
            # Create the directory if it does not exist
            os.makedirs(result_dir, exist_ok=True)

            result_file = os.path.join(result_dir, f"{checkpoint_file}.txt")
            
            if os.path.exists(result_file):
                continue  # Skip this checkpoint if its evaluation result already exists
            command = f"python evaluate.py --landlord {os.path.join(landlord_weights, checkpoint_file)} --landlord_up {landlord_up} --landlord_down {landlord_down}"
            with open(result_file, "w") as f:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                output, _ = process.communicate()
                f.write(output.decode())
            print(f"Finished evaluating {checkpoint_file}.")

save_dir = "./evaluate_result"

os.makedirs(save_dir, exist_ok=True)

# ADP vs Random, SL, rlcard
# run_evaluate("./douzero_checkpoints/douzero", "random", "random", save_dir)
# run_evaluate("./douzero_checkpoints/douzero", "baselines/sl/landlord_up.ckpt", "baselines/sl/landlord_down.ckpt", save_dir)
# run_evaluate("./douzero_checkpoints/douzero", "rlcard", "rlcard", save_dir)

# WP vs Random, SL, rlcard
# run_evaluate("./douzero_checkpoints_wp/douzero", "random", "random", save_dir)
# run_evaluate("./douzero_checkpoints_wp/douzero", "baselines/sl/landlord_up.ckpt", "baselines/sl/landlord_down.ckpt", save_dir)
run_evaluate("./douzero_checkpoints_wp/douzero", "rlcard", "rlcard", save_dir)
