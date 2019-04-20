import pandas as pd
import os
import re
import numpy as np
from collections import defaultdict
def main():
    path = '../Characters_directory/'
    characters_dir = os.listdir(path)
    columns = []
    name_entities_dictionary = defaultdict(list)
    for file in characters_dir:
        pattern = r'(.+?)\.'
        name = re.findall(pattern,file)[0]
        columns.append(name)
        f = open(path + file, 'r')
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            if len(line):
                name_entities_dictionary[name].append(line)

    whole_possible_name_entities_list = []
    for i in name_entities_dictionary.values():
        for j in i:
            whole_possible_name_entities_list.append(j)

    ##List to numpy because of efficiency
    whole_possible_name_entities = np.array(whole_possible_name_entities_list)
    print(whole_possible_name_entities)



if __name__ == '__main__':
    main()
