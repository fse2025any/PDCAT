import os,sys
import random, time, copy,subprocess, argparse
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

def get_objective_score(independent, k_iter, SOURCE_PATH, GCC_PATH, INCLUDE_PATH, EXEC_PARAM, LOG_FILE, all_flags):
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
    return (time_o3_c /time_c)

def data_process_line(file_path):
    """
    obtain data like ([0,1,...,1], 1.1)
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            sequence_part, per_part = line.strip().split('-')
            sequence = [int(x) for x in sequence_part.split(',')]
            value = float(per_part)  
            data.append((sequence, value))
    return data

def extract_sequences(data):
    """
    obtain sequences whose performance > 1.0
    """
    extracted_sequences = []
    for item in data:
        sequence, value = item
        if value > 1.0:
            extracted_sequences.append(sequence)
    return extracted_sequences

def read_flags_from_file(file_path):
    """
    obtain all flags
    """
    with open(file_path, 'r') as file:
        flags = file.read().strip()
    return [flag.strip() for flag in flags.split(',') if flag.strip()]

def parse_constraints(file_path):
    strong_dependency = []
    weak_dependency = []
    synergistic_relationship = []
    current_category = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Strong dependency:"):
            current_category = "strong_dependency"
        elif line.startswith("Weak dependency:"):
            current_category = "weak_dependency"
        elif line.startswith("Synergistic relationship:"):
            current_category = "synergistic_relationship"
        elif line:
            if "->" in line:
                constraints = [item.strip() for item in line.replace("->", ",").split(",")]
            elif "and" in line:
                constraints = [item.strip() for item in line.replace("and", ",").split(",")]
            else:
                continue
            if current_category == "strong_dependency":
                strong_dependency.append(constraints)
            elif current_category == "weak_dependency":
                weak_dependency.append(constraints)
            elif current_category == "synergistic_relationship":
                synergistic_relationship.append(constraints)
    return {
        "strong_dependency": strong_dependency,
        "weak_dependency": weak_dependency,
        "synergistic_relationship": synergistic_relationship
    }


class PDCAT:
    def __init__(self, a, b, c, get_objective_score, source_path, gcc_path, include_path, exec_param, log_file, flags, seqs, constraints):
        """
        :param a: parameter of initial process
        :param b: parameter of initial process
        :param c: parameter of tuning process
        :param get_objective_score: obtain true speedup
        :param source_path: program's path
        :param gcc_path: gcc's path
        :param include_path: header file for program
        :param exec_param: exection paramter
        :param log_file: record results
        :param flags: all flags
        :param seqs: all initial tuning sequences
        :param constraints: three type constraints
        """
        self.a = a
        self.b = b
        self.c = c
        self.proini = []
        self.get_objective_score = get_objective_score 
        self.SOURCE_PATH = source_path
        self.GCC_PATH = gcc_path
        self.INCLUDE_PATH = include_path
        self.EXEC_PARAM = exec_param
        self.LOG_FILE = log_file
        self.all_flags = flags
        self.initial_seqs = seqs
        self.initial_pro = self.Obtain_initial_pro()
        self.constraints = constraints

    def constraints_check(self, seq):
        """
        Check sequence constraints
        """
        flag = False
        strong_dependency = self.constraints['strong_dependency']
        weak_dependency = self.constraints['weak_dependency']
        synergistic_relationship = self.constraints['synergistic_relationship']
        # strong dependcy check
        for i in range(len(strong_dependency)):
            if strong_dependency[i][0] in self.all_flags and strong_dependency[i][1] in self.all_flags:
                idx1 = self.all_flags.index(strong_dependency[i][0])
                idx2 = self.all_flags.index(strong_dependency[i][1])
                if seq[idx1] == 0 and seq[idx2] == 1:
                    flag = True
                else:
                    continue
            else:
                continue
        # weak dependcy check
        for i in range(len(weak_dependency)):
            if 'and' in weak_dependency[i][0]:
                two_flag = weak_dependency[i][0].split(' and ')
                if two_flag[0] in self.all_flags and two_flag[1] in self.all_flags and weak_dependency[i][1] in self.all_flags:
                    idx1 = self.all_flags.index(two_flag[0])
                    idx2 = self.all_flags.index(two_flag[1])
                    idx3 = self.all_flags.index(weak_dependency[i][1])
                    if (seq[idx1] == 1 and seq[idx2] == 1) and seq[idx3] == 0:
                        flag = True
                    else:
                        continue
                else:
                    continue
            else:
                if weak_dependency[i][0] in self.all_flags and weak_dependency[i][1] in self.all_flags:
                    idx1 = self.all_flags.index(weak_dependency[i][0])
                    idx2 = self.all_flags.index(weak_dependency[i][1])
                    if seq[idx1] == 1 and seq[idx2] == 0:
                        flag = True
                    else:
                        continue
                else:
                    continue
        # synergistic relationship check
        for i in range(len(synergistic_relationship)):
            if synergistic_relationship[i][0] in self.all_flags and synergistic_relationship[i][1] in self.all_flags:
                idx1 = self.all_flags.index(synergistic_relationship[i][0])
                idx2 = self.all_flags.index(synergistic_relationship[i][1])
                if ((seq[idx1] == 1 and seq[idx2] == 0) or (seq[idx1] == 0 and seq[idx2] == 1)):
                    flag = True
                else:
                    continue
            else:
                continue
        return flag
    
    def Obtain_initial_pro(self):
        return [random.uniform(0, 1) for _ in range(len(self.all_flags) - 47)]

    def transProbtoflags(self, prob):
        """
        Enable flags as enable probabilities
        """
        enable_state = []
        for p in prob:
            if random.random() < p:
                enable_state.append(1)
            else:
                enable_state.append(0)
        return enable_state

    def run(self):
        ts = []   # time consumption
        res = []  # speedup for different flag combinations
        seqs = [] # different flag combinations
        ts.append(0)
        time_zero = time.time()
        flag = True
        permin = 0.0
        permax = 0.0
        Es = []
        common_flags =  [1] * 47 # -O1 flag number 97 109
        while ts[-1] < 5000:
            explored_flags = self.transProbtoflags(self.initial_pro)
            seq = common_flags + explored_flags
            while(self.constraints_check(seq)):
                explored_flags = self.transProbtoflags(self.initial_pro)
                seq = common_flags + explored_flags
            E = 0.0
            seqs.append(seq)
            if(flag):
                temp = self.get_objective_score(seq, len(ts), SOURCE_PATH=self.SOURCE_PATH, GCC_PATH=self.GCC_PATH, INCLUDE_PATH=self.INCLUDE_PATH, EXEC_PARAM=self.EXEC_PARAM, LOG_FILE=self.LOG_FILE, all_flags=self.all_flags)
                res.append(temp)
                permin = min(1.0, temp)
                permax = max(1.0, temp)
                E = (temp - permin) / (permax - permin)
                Es.append(E)
                flag = False
            else:
                temp = self.get_objective_score(seq, len(ts), SOURCE_PATH=self.SOURCE_PATH, GCC_PATH=self.GCC_PATH, INCLUDE_PATH=self.INCLUDE_PATH, EXEC_PARAM=self.EXEC_PARAM, LOG_FILE=self.LOG_FILE, all_flags=self.all_flags)
                res.append(temp)
                permin = min(permin, temp)
                permax = max(permax, temp)
                E = (temp - permin) / (permax - permin)
                Es.append(E)
            if E > sum(Es)/len(Es):
                for i in range(len(self.initial_pro)):
                    self.initial_pro[i] = self.initial_pro[i] + self.c * (1 - self.initial_pro[i])
            else:
                for i in range(len(self.initial_pro)):
                    self.initial_pro[i] = self.initial_pro[i] - self.c * self.initial_pro[i]
            time_now = time.time()
            ts.append(time_now-time_zero)
            best_result = max(res)
            best_seq = seqs[res.index(best_result)]
            ss = '{}: cur-best {}, cur-best-seq {}'.format(str(round(ts[-1])), str(best_result), str(best_seq))
            write_log(ss, self.LOG_FILE)


if __name__ == "__main__":
    LOG_DIR = 'log' + os.sep

    if not os.path.exists(LOG_DIR):
        os.system('mkdir '+LOG_DIR)

    parser = argparse.ArgumentParser(description="Preference-Driven Compiler Auto-Tuning")
    
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
    
    parser.add_argument("--sequences_path", type=str, required=True,
                        help="Initial tuning data")
    
    parser.add_argument("--constraints_path", type=str, required=True,
                        help="Three type constraints")
    
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

    all_constraints = parse_constraints(args.constraints_path)
    per_data = data_process_line(args.sequences_path)
    good_sequence = extract_sequences(per_data)
    pdcat_params = {}
    pdcat_params['get_objective_score'] = get_objective_score
    pdcat_params['a'] = 1
    pdcat_params['b'] = 1
    pdcat_params['c'] = 0.5
    pdcat_params['source_path'] = args.source_path
    pdcat_params['gcc_path'] = args.gcc_path
    pdcat_params['include_path'] = '-I /home/user/polybench-code/utilities /home/user/polybench-code/utilities/polybench.c'
    pdcat_params['exec_param'] = args.exec_param
    LOG_DIR = 'log' + os.sep
    LOG_FILE = LOG_DIR +  args.log_file
    pdcat_params['log_file'] = LOG_FILE
    pdcat_params['flags'] = all_flags
    pdcat_params['seqs'] = good_sequence
    pdcat_params['constraints'] = all_constraints
    pd = PDCAT(**pdcat_params)
    pd.run()