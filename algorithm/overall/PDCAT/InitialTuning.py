import os,sys,argparse
import random, time, copy,subprocess
import math
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from scipy.stats import norm


def write_log(ss, file):
    """ Write to log """
    with open(file, 'a') as log:
        log.write(ss + '\n')

def execute_terminal_command(command):
    """ Execute command """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout:
                print("命令输出：")
                print(result.stdout)
        else:
            if result.stderr:
                print("错误输出：")
                print(result.stderr)
    except Exception as e:
        print("执行命令时出现错误：", str(e))

def get_objective_score(independent, SOURCE_PATH, GCC_PATH, INCLUDE_PATH, EXEC_PARAM, LOG_FILE, all_flags):
    """ Obtain the speedup """
    opt = ''
    for i in range(len(independent)):
        if independent[i]:
            opt = opt + all_flags[i] + ' '
        else:
            negated_flag_name = all_flags[i].replace("-f", "-fno-", 1)
            opt = opt + negated_flag_name + ' '
    command = f"{GCC_PATH} -O2 {opt} -c {INCLUDE_PATH} {SOURCE_PATH}/*.c"
    execute_terminal_command(command)
    command2 = f"{GCC_PATH} -o a.out -O2 {opt} -lm *.o"
    execute_terminal_command(command2)
    time_start = time.time()
    command3 = f"./a.out {EXEC_PARAM}"
    execute_terminal_command(command3)
    time_end = time.time()  
    cmd4 = 'rm -rf *.o *.I *.s a.out'
    execute_terminal_command(cmd4)
    time_c = time_end - time_start   #time opt
    time_o3 = time.time()
    command = f"{GCC_PATH} -O3 {opt} -c {INCLUDE_PATH} {SOURCE_PATH}/*.c"
    execute_terminal_command(command)
    command2 = f"{GCC_PATH} -o a.out -O3 -lm *.o"
    execute_terminal_command(command2)
    time_o3 = time.time()
    command3 = "./a.out {EXEC_PARAM}"
    execute_terminal_command(command3)
    time_o3_end = time.time()  
    cmd4 = 'rm -rf *.o *.I *.s a.out'
    execute_terminal_command(cmd4)
    time_o3_c = time_o3_end - time_o3   #time o3
    op_str = "{}-{}".format(str(independent), str(time_o3_c /time_c))
    write_log(op_str, LOG_FILE)
    return (time_o3_c /time_c)

def read_flags_from_file(file_path):
    with open(file_path, 'r') as file:
        flags = file.read().strip()
    return [flag.strip() for flag in flags.split(',') if flag.strip()]

def constraints_check(seq):
    """
    Check sequence constraints
    """
    return False

def generate_random_conf(x, all_flags):
    """ Generation 0-1 mapping for disable-enable options """
    comb = bin(x).replace('0b', '')
    comb = '0' * (len(all_flags) - len(comb)) + comb
    conf = [int(s) for s in comb]
    return conf

if __name__ == "__main__":
    LOG_DIR = 'log' + os.sep

    if not os.path.exists(LOG_DIR):
        os.system('mkdir '+LOG_DIR)

    parser = argparse.ArgumentParser(description="Initial Tuning on Selected Programs")
    
    parser.add_argument("--log_file", type=str, required=True,
                        help="File to save log")
    
    parser.add_argument("--source_path", type=str, required=True,
                        help="Path to the source program for tuning")
    
    parser.add_argument("--gcc_path", type=str, required=True,
                        help="Path of compiler")
    
    parser.add_argument("--exec_param", type=str, default=None,
                        help="Execution parameter for the output executable (can be empty)")
    
    
    parser.add_argument("--flag_path", type=str, required=True,
                        help="Tuning flags file")
    
    
    
    args = parser.parse_args()
    if args.exec_param:
        EXEC_PARAM = args.exec_param
    else:
        EXEC_PARAM = '' 

    LOG_FILE = LOG_DIR +  args.log_file

    if args.flag_path:
        all_flags = read_flags_from_file(args.flag_path)
    else:
        all_flags = ['-O2']
        print('No flags')

    seqs = []
    
    #include_path can be empty
    include_path = '-I /home/user/polybench-code/utilities /home/user/polybench-code/utilities/polybench.c'
    while(len(seqs) < 500):
        x = random.randint(0, 2 ** len(all_flags) - 1)
        seq = generate_random_conf(x, all_flags)
        if(constraints_check(seq) == False):
            seqs.append(seq)
        else:
            continue

    for i in range(len(seqs)):
        per = get_objective_score(seqs[i], args.source_path, args.gcc_path, include_path, EXEC_PARAM, LOG_FILE, all_flags)