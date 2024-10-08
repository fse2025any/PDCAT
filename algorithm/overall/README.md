In this repository, we provide our code for overall comparison.


## Techniques


### The folder `overall` contains all the techniques code for overall experiment.

The `RIO.py` is the code for **Random Iterative Optimization**. For example, if you want to use it to tune program `correlation`, you can input command `python RIO.py --log_file=correlation_rio.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt`.
In this command, `--log_file` is your log file name, `--source_path` is your program path, `--gcc_path` is your compiler path, and `--flag_path` is for your tuning optimization flags. Moreover, if your program has parameters, you need to input `--exec_param`. 

The `CompTuner.py` is the code for **Compiler Autotuning through Multiple Phase Learning**. For example, if you want to use it to tune program `correlation`, you can input command `python CompTuner.py --log_file=correlation_comptuner.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt`.
In this command, `--log_file` is your log file name, `--source_path` is your program path, `--gcc_path` is your compiler path, and `--flag_path` is for your tuning optimization flags. Moreover, if your program has parameters, you need to input `--exec_param`. 

The folder `CFCSA` is the code for **Compiler Auto-tuning via Critical Flag Selection**, which contains `getrelated.py` and `CFSCA.py`. For example, if you want to use it to tune program `correlation`, you firstly need run `getrelated.py` as command `python getrelated.py --source_path=/home/user/polybench-code/datamining/correlation --flag_path=/home/user/flag.txt`, to obtain the related flags of the target program. Then you can input command `python CFSCA.py --log_file=correlation_cfsca.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --related_flags=1,2,3,4,5,6,7,8,9,10`.
In this command, `--log_file` is your log file name, `--source_path` is your program path, `--gcc_path` is your compiler path, `--related_flags` are related flags' index, and `--flag_path` is for your tuning optimization flags. Moreover, if your program has parameters, you need to input `--exec_param`. 

The folder `PDCAT` is the code for **PDCAT: Preference-Driven Compiler Auto-Tuning**, which contains `constraints.txt`, `InitialTuning.py` and `PDCAT.py`. `constraints.txt` contains collected combined constraints. `InitialTuning.py` is for obtaining initial tuning data, you can input command `InitialTuning.py`.
If you want to use it to tune program `correlation`, you can input command `python PDCAT.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt`.
In this command, `--log_file` is your log file name, `--source_path` is your program path, `--gcc_path` is your compiler path, `--sequences_path` is initial tuning data, and `--flag_path` is for your tuning optimization flags. Moreover, if your program has parameters, you need to input `--exec_param`. 