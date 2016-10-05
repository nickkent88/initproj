import json
import os
import simplejson

# Parse tree recursively
def make_structure(json_file_path):
    with open(json_file_path) as json_file:
        tree = simplejson.load(json_file)
        parse_tree(tree)

def parse_tree(json_dict):
    for item in json_dict.items():
        key = item[0]
        value = item[1]
        if isinstance(value, dict):
            dirname = key
            make_directory(value, dirname)
        if isinstance(value, basestring):
            filename = key
            make_file(filename)

def make_directory(json_dict, dirname):
    print("Dir: {}".format(dirname))
    # make dir
    parse_tree(json_dict)
    # os.mkdir(dirname)

def make_file(filename):
    print("File: {}".format(filename))
    # make file

if __name__ == "__main__":
    make_structure(r'../templates/sample.json')