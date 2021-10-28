#!/usr/bin/env python3
import csv
import os.path
import argparse

description = '''
This script takes a .txt file and sort it hierarchically
based on its properties and user defined metric field
'''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-p', '--path', action='store', dest='file_path', required=True, help='The path your file .txt is located')
parser.add_argument('-s', '--sep', action='store', dest='delimiter', default='|', help='Separator character in .txt file \nDefault: "|" (pipe)')

def main(file_path, delimiter):
    ## Read file data.txt
    input_file = read_file(file_path, delimiter)
    
    ## Sort file based on hierarchy
    sorted_file = sort_data(input_file)

    ## Write file to .txt using pipe delimiter
    write_file(file_path, sorted_file)

def read_file(file_path, delimiter):
    with open (file_path, 'r') as input_file:
        return list(csv.DictReader(input_file, delimiter=delimiter))

def replace_value(input_file, value_from, value_to):
    new_list = []
    for i, x in enumerate(input_file):
        for key, value in x.items():
            if value == value_from:
                x[key] = value_to
        new_list.append(x)
    return new_list

def sort_data(input_file):
    return sorted(replace_value(input_file,'$total','ztotal'), key=lambda d: (d['property0'],d['property1'],d['property2'],d['net_sales']), reverse=True) 

def write_file(file_path, sorted_file):
    path, extension = os.path.splitext(file_path)
    with open(path+'_out'+extension, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(
            output_file, 
            fieldnames=sorted_file[0].keys(),
            delimiter='|'
        )
        fc.writeheader()
        fc.writerows(replace_value(sorted_file,'ztotal','$total'))

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.file_path, args.delimiter)


## Not finished - Dynamically find file properties and specify a metric to sort 

# ## Get list of properties existed on input_file
# sort_order = get_properties(input_file)

# def get_properties(input_file):
#     ## Search for last hierarquical property 
#     keys = list(input_file[0].keys())
#     last = find_last_occurence(keys,'property')

#     ## Create a list based on the amount of properties existed on data.txt
#     index_list = [str(i).zfill(1) for i in range(last+1)]
#     property_list = ['property'] * (last+1)
    
#     return [i + j for i, j in zip(property_list, index_list)]

# def find_last_occurence(searched_list, value):
#     for i in reversed(range(len(searched_list))):
#         if value in searched_list[i]:
#             return i
#     raise ValueError("{} is not in list".format(x))