import os
import re
import subprocess

def convert_to_numeric(string):
    patternM = r'^(\d+(\.\d+)?)M$'
    patternK = r'^(\d+(\.\d+)?)K$'
    matchM = re.match(patternM, string)
    matchK = re.match(patternK, string)
    if matchM:
        return float(matchM.group(1))
    elif matchK:
        return float(matchK.group(1)) / 1000
    return None

documents_folder = "../../Documents"

directories = [os.path.join(documents_folder, d) for d in os.listdir(documents_folder) if os.path.isdir(os.path.join(documents_folder, d))]

sizes = []

for directory in directories:
    command = ['du', '-sh', directory]
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        size, path = output.strip().split('\t')
        sizes.append([size, path])
    except subprocess.CalledProcessError as e:
        print(f'Error executing {e}')
    
for comb in sizes:
    to_replace_with = convert_to_numeric(comb[0])
    comb[0] = to_replace_with

sizes.sort(key=lambda x: x[0], reverse=True)
        
for comb in sizes:
    if comb[0] < 1:
        print(f'{comb[1]:<30} {comb[0]*1000:>15.2f}KB')
    else:
        print(f'{comb[1]:<30} {comb[0]:>15.2f}MB')