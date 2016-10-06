import json
import os
# import simplejson

class TreeParser(object):
    """docstring for TreeParser"""
    def __init__(self, current_dir, json_file_path):
        super(TreeParser, self).__init__()
        self.path_stack = [current_dir]
        with open(json_file_path) as json_file:
            self.tree_dict = json.load(json_file)
            # When we add a directory, we will push its name on the stack
            # When we leave the directory, we will pop it
            # We get the path at which files are being created by joining the elements
            # of the stack

# Parse tree recursively
    def make_structure(self):
            self.parse_tree(self.tree_dict)

    def parse_tree(self, json_dict):        
        for key, value in sorted(json_dict.items()):
            if isinstance(value, dict):
                dirname = key
                self.make_directory(dirname, value)
            if isinstance(value, basestring):
                filename = key
                self.make_file(filename)

    def make_directory(self, dirname, json_dict):
        self.path_stack.append(dirname)
        path = os.path.join(*self.path_stack)
        if not os.path.isdir(dirname):
            print("Dir: {}".format(path))
            os.mkdir(path)
        self.parse_tree(json_dict)
        self.path_stack.pop()
        

    def make_file(self, filename):
        self.path_stack.append(filename)
        path = os.path.join(*self.path_stack)
        print("File: {}".format(path))
        open(path, 'a').close()
        self.path_stack.pop()

if __name__ == "__main__":
    parsey_mc_parseface = TreeParser(r'.', r'../templates/sample.json')
    parsey_mc_parseface.make_structure()