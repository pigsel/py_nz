# to parse structures files and collect data about insulators
from pathlib import Path
import pandas as pd


workdir = Path(r'C:\_Igor_\python\py_nz\parse_str')  # working directory
p_sttab = workdir / 'staking_table.txt'  # path to staking table
p_str = workdir / 'temp.stk'  # path to structures files


def stk_read(path):
    # read stk files
    with open(path, newline='') as stk_file:
        lines = stk_file.readlines()
        str_type = lines[0].split("'")[1]
        str_description = lines[1]
        str_height = float(lines[4].split()[0])
        sets = {}  # dictionary to hold sets
        #print(f"Structure type: {str_type}")
        #print(f"Description: {str_description.strip()}")
        #print(f"Height: {str_height}")  
    
        i = 6
        while i != "S":
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
                i="S"
            else:
                #print("Unexpected line format:", lines[i])
                i += 1
    return sets


print(stk_read(p_str))
Str_id = 'T1'  # structure ID

df = pd.DataFrame(stk_read(p_str)).T  # transpose to have sets as rows
df.columns = ['Type', 'Weight', 'Wind Area', 'Length']  # add column names
df = df.reset_index().rename(columns={'index': 'Set'})  # add set names as first column
df.insert(0, 'Str_id', Str_id)  # insert column with same value for all rows
print(df)
