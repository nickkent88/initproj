import json
import logging
import os

from shutil import copyfile

GITIGNORE_DIR = "../fixtures/gitignores/"
LICENSE_DIR = "../fixtures/licenses/"

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logger.basicConfig(format=FORMAT, level=logger.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        logger.debug('make_structure()')
        self.parse_tree(self.tree_dict)

    def parse_tree(self, json_dict):  
        logger.debug('parse_tree()')

        for key, value in sorted(json_dict.items()):
            if isinstance(value, dict): # A directory
                dirname = key
                self.make_directory(dirname, value)
            else: # A file
                filename = key
                _, extension = os.path.splitext(' ' + filename)
                logger.debug(extension)
                handle_file = self.file_dispatch.get(
                    extension, self.make_file)
                option = value
                handle_file(filename, option)

    def make_directory(self, dirname, json_dict):
        logger.debug('make_directory()')
        path = self.path_from_stack(dirname)
        if not os.path.isdir(path):
            logger.debug("Dir: {}".format(path))
            os.mkdir(path)
        else:
            logger.debug("Directory {} already exists.".format(path))
        self.parse_tree(json_dict)
        self.path_stack.pop()
        

    def make_file(self, filename, option=None):
        logger.debug('make_file()')
        path = self.path_from_stack(filename)
        if not os.path.isfile(path):
            logger.info("File: {}".format(path))
        else:
            logger.info("File {} already exists.".format(path))
        open(path, 'a').close()
        self.path_stack.pop()

    def make_gitignore(self, filename, language=None):
        logger.debug('make_gitignore()')
        logger.debug(filename)
        logger.info("Making {}.gitignore.".format(language))
        # filename = '.'.join((language, 'gitignore'))
        # gitignore_path = os.path.join(GITIGNORE_DIR, filename)
        # path = self.path_from_stack(filename)
        # copyfile(gitignore_path, path)

    def path_from_stack(self, filename):
        self.path_stack.append(filename)
        return os.path.join(*self.path_stack)



if __name__ == "__main__":
    parsey_mc_parseface = TreeParser(r'.', r'../templates/sample.json')
    parsey_mc_parseface.make_structure()