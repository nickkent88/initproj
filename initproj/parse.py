import json
import os

from shutil import copyfile

class TreeParser(object):
    """docstring for TreeParser"""
    def __init__(self, current_dir, json_file_path):
        super(TreeParser, self).__init__()
        self.path_stack = [current_dir]
        with open(json_file_path) as json_file:
            self.tree_dict = json.load(json_file)
            # Dispatch dict can be used to handle certain file types in special 
            # ways.
            self.file_dispatch = {
                ".gitignore": self.make_gitignore
            }

# Parse tree recursively
    def make_structure(self):
            self.parse_tree(self.tree_dict)

    def parse_tree(self, json_dict):        
        for key, value in sorted(json_dict.items()):
            if isinstance(value, dict): # A directory
                dirname = key
                self.make_directory(dirname, value)
            else: # A file
                filename = key
                _, extension = os.path.splitext(' ' + filename)
                print(extension)
                handle_file = self.file_dispatch.get(
                    extension, self.make_file)
                option = value
                handle_file(filename, option)

    def make_directory(self, dirname, json_dict):
        self.path_stack.append(dirname)
        path = os.path.join(*self.path_stack)
        if not os.path.isdir(path):
            print("Dir: {}".format(path))
            os.mkdir(path)
        else:
            print("Directory {} already exists.".format(path))
        self.parse_tree(json_dict)
        self.path_stack.pop()
        

    def make_file(self, filename, option=None):
        path = self.path_from_stack(filename)
        if not os.path.isfile(path):
            print("File: {}".format(path))
        else:
            print("File {} already exists.".format(path))
        open(path, 'a').close()
        self.path_stack.pop()

    def make_gitignore(self, filename, language=None):
        print("Making {}.gitignore.".format(language))


    def path_from_stack(self, filename):
        self.path_stack.append(filename)
        return os.path.join(*self.path_stack)



if __name__ == "__main__":
    parsey_mc_parseface = TreeParser(r'.', r'../templates/sample.json')
    parsey_mc_parseface.make_structure()