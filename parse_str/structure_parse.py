# to parse structures files and collect data about insulators
from pathlib import Path
import pandas as pd

# define class to hold insulator data
Insulator = {} # name, str_name, set_name, set_label, ins_type, weight, wind_area, length, azimuth, description, pls_set, pls_strain
Structure = {} # name, str_description, str_type, str_contract, str_function, ins_list
 

workdir = Path(r'C:\_Igor_\python\py_nz\parse_str')  # working directory
p_sttab = workdir / 'staking_table.txt'  # path to staking table
p_str = workdir / 'test_strain.POL'  # path to structures files


def stk_read(path):
    # read stk files
    with open(path, newline='') as stk_file:
        lines = stk_file.readlines()
        sets = {}  # dictionary to hold sets
    
        i = 6
        while i < 1000:
            if lines[i].startswith("'") and lines[i].split("'")[1] != "":
                set_name = lines[i].split("'")[1]
                if not lines[i].split("'")[3] == "C":
                    sets[set_name] = [lines[i].split("'")[3], lines[i+1].split()[0], lines[i+1].split()[1], lines[i+1].split()[2]]
                # add set and its parameters to dictionary: [ins type (I = susp, S = strain, C = clamp), ins weight, wind area, length])]
                else:
                    sets[set_name] = [lines[i].split("'")[3], 0, 0, 0]
                    # for clamps, length is not applicable
                i += 1
            elif lines[i].startswith("S"):
                #print("End of sets")
                i=1000
            else:
                #print("Unexpected line format:", lines[i])
                i += 1
    return sets


# print(stk_read(p_str))
# Str_id = 'T1'  # structure ID

# df = pd.DataFrame(stk_read(p_str)).T  # transpose to have sets as rows
# df.columns = ['Type', 'Weight', 'Wind Area', 'Length']  # add column names
# df = df.reset_index().rename(columns={'index': 'Set'})  # add set names as first column
# df.insert(0, 'Str_id', Str_id)  # insert column with same value for all rows
# print(df)


def towerpole_read(path):
    # read pole files
    with open(path, newline='') as pole_file:
        lines = pole_file.readlines()
        inss = {}  # dictionary to hold setsinsulators
        Clamps = 0
        Susp = 0
        Strain = 0
        Post = 0
        TwoPart = 0
        ini_file = None

        for i, line in enumerate(lines):
            if line.strip().endswith(".inl"):
                print(f"Line {i}: {line}")  # prints line number and content
                ini_file = Path(line.strip())
                break
        
    return ini_file
