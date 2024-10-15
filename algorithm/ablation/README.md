In this repository, we provide our code for overall comparison.


## Techniques


### The folder `ablation` contains all the techniques code for overall experiment.

The folder `initial_enable_probabilities_aqc` is the code for RQ1, which contains `PDCAT_no_initial.py` (i.e., PDCAT without initial enable probabilities acquisition phase). If you want to use it to tune program `correlation`, you can input command `python PDCAT_no_initial.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt --constraints_path=/home/user/constraints.txt`.


The folder `tuning_on_program` is the code for RQ2, which contains `PDCAT_no_tuning.py` (i.e., PDCAT without tuning phase). If you want to use it to tune program `correlation`, you can input command `python PDCAT_no_tuning.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt --constraints_path=/home/user/constraints.txt`.


The folder `combined_optimization_analysis` is the code for RQ3, which contains `PDCAT_nocheck.py` (i.e., PDCAT without combined optimization analysis). If you want to use it to tune program `correlation`, you can input command `python PDCAT_nocheck.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt`; `CompTuner_check.py` (i.e., CompTuner with combined optimization analysis). If you want to use it to tune program `correlation`, you can input command `python CompTuner_check.py --log_file=correlation_comptuner.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --constraints_path=/home/user/constraints.txt`; `CFSCA_check.py` (i.e., i.e., CFSCA with combined optimization analysis). If you want to use it to tune program `correlation`, you firstly need run `getrelated.py` as command `python getrelated.py --source_path=/home/user/polybench-code/datamining/correlation --flag_path=/home/user/flag.txt`, to obtain the related flags of the target program. Then you can input command `python CFSCA_check.py --log_file=correlation_cfsca.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --related_flags=1,2,3,4,5,6,7,8,9,10 --constraints_path=/home/user/constraints.txt`.


The folder `common_optimization` is the code for RQ4, which contains `PDCAT_allexp.py` (i.e., PDCAT without common optimization). If you want to use it to tune program `correlation`, you can input command `python PDCAT_allexp.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt --constraints_path=/home/user/constraints.txt`; `PDCAT_o2.py` (i.e., PDCAT with common optimization -O2). If you want to use it to tune program `correlation`, you can input command `python PDCAT_o2.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt --constraints_path=/home/user/constraints.txt`; `PDCAT_o3.py` (i.e., PDCAT without common optimization -O3). If you want to use it to tune program `correlation`, you can input command `python PDCAT_o3.py --log_file=correlation_pdcat.log --source_path=/home/user/polybench-code/datamining/correlation --gcc_path=gcc --flag_path=/home/user/flag.txt --sequences_path=/home/user/inidata.txt --constraints_path=/home/user/constraints.txt`; 



