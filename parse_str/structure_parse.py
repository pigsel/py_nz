# to parse structures files and collect data about insulators
# the idea is to fill a dict with structures, write wich ins they have
# and it will linked to another dict with insulators db
# during parsing, we collect all used ins sets and their parameters
#

from pathlib import Path
import pandas as pd

# define dict to hold insulator data
Insulator = {} # name, str_name, set_name, set_label, ins_type, weight, wind_area, length, azimuth, description, pls_set, pls_strain
Structure = {} # name, str_description, str_type, str_contract, str_function, ins_list
ins_types = {'C': ['Clamp', 0], 'I': ['Suspension', 0], 'S': ['Strain', 0], 'P': ['Post', 0], 'T': ['2-Parts', 0]} # insulator types and their counts 

workdir = Path(r'C:\_Igor_\python\py_nz\parse_str')  # working directory
p_sttab = workdir / 'sttable.txt'  # path to staking table
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


def towerpole_read(path):
    # read pole files
    with open(path, newline='') as pole_file:
        lines = pole_file.readlines()
        ini_file = None
        s = 0
        selected_strokes = []

        # 1 finding line No with .inl file and ini file path
        for i, line in enumerate(lines):
            if line.strip().endswith(".inl"):
                print(f"Line {i}: {line}")  # prints line number and content
                ini_file = Path(line.strip())
                s = i+1 # start collecting strokes from next line
                break
        
        # 2 collecting strokes with insulators
        while s < 1000:
            # find line with 'end' - after that plscadd ini links written
            if lines[s].strip().endswith("end"):
                selected_strokes.append(lines[s].strip()) # collect line with 'end'
                print("end found")
                s += 1
                while s < 1000:
                    if lines[s].startswith("'"):
                        selected_strokes.append(lines[s].strip())
                        # print(lines[s].strip())
                        s += 1
                    else:
                        #print(lines[s].strip())
                        print('end')
                        s=1000  # exit loop
                        break
            else:
                # collect lines with insulators
                selected_strokes.append(lines[s].strip())
                s += 1

        # 3 parse collected strokes
        for ins in ins_types.keys():
            for stroke in selected_strokes:
                if len(stroke) > 0:
                    if stroke.split()[2] == ins_types[ins][0]:
                        ins_types[ins][1] = stroke.split()[0]
        print(ins_types)

#towerpole_read(p_str)

# creating dataframes for structures and for insulators

# df = pd.DataFrame(stk_read(p_str)).T  # transpose to have sets as rows
# df.columns = ['Type', 'Weight', 'Wind Area', 'Length']  # add column names
# df = df.reset_index().rename(columns={'index': 'Set'})  # add set names as first column
# df.insert(0, 'Str_id', Str_id)  # insert column with same value for all rows
# print(df)