import os
import json
import yaml

class Pathfinder:
    """Tool for loading configuration files in .yml or .json

    Designed to use a json or yml file as "path library", getting
    the desired value with Pathfinder[Keyword].

    Can return nested dictionaries using dot separated values like
    Pathfinder[Dict.Nested_Dict.Keyword].

    Changes default dictionary using Pathfinder.select() method.

    Use Pathfinder.get() to always return from loaded file 
    (ignoring any selected nested dictionary).

    Parameters
    ----------
    file_path : str, default None.
        If NoneType, load configuration from ~/config/configuration.yml or .json.

        If ListType, load and merge dicts in listed string file paths.
        Identical keywords will be replaced by the forwardmost loaded file on list.
    """

    def __init__(self, file_path:str = None):
        # Original data from file
        self._build_original(file_path)
        # Selected data (can be changed with methods)
        self.data = self.original

    def __getitem__(self, keyword:str):
        return self.keyword_dot(self.data, keyword)

    def _build_original(self, file_path):
        """Set self.original dictionary build.
        """
        if file_path == None:
            self.original = self._load_default()
        elif isinstance(file_path, str):
            self.original = self._load_from_file(file_path)
        elif isinstance(file_path, list):
            self.original = self._load_from_list(file_path)
        else:
            raise TypeError("file_path must be either None, string or a list of strings")

    @staticmethod
    def read_json_file(file_path:str):
        """Read json file.

        Returns parsed json file.
        """
        # Get relative path from current working directory
        rel_path = os.path.relpath(file_path)
        parsed_json = json.load(open(rel_path))
        return parsed_json

    @staticmethod
    def read_yml_file(file_path:str):
        """Read yml file using yaml.SafeLoader.

        Returns parsed yml file.
        """
        # Get relative path from current working directory
        rel_path = os.path.relpath(file_path)
        parsed_yml = yaml.load(open(rel_path), Loader=yaml.SafeLoader)
        return parsed_yml

    def _load_from_file(self, file_path:str):
        """Load data from file_path.
        """
        # Get file format from string
        file_format = file_path.split(sep='.')[-1]

        if file_format == 'yml' or file_format == 'yaml':
            data = self.read_yml_file(file_path)
            return data
        elif file_format == 'json':
            data = self.read_json_file(file_path) 
            return data       
        else:
            raise Exception("Wrong file format. Use yml/yaml or json files")

    def _load_default(self):
        """Load configuration from ~/config/configuration.yml or .json if file_path == None.

        Returns loaded data from file_path.
        """
        default_path = "config/configuration"
        try:
            data = self._load_from_file(default_path + ".yml")
        except FileNotFoundError:
            try:
                data = self._load_from_file(default_path + ".json")
            except FileNotFoundError:                  
                raise Exception("Could not find configuration.yml or .json in ~/config/")
        return data

    def _load_from_list(self, file_path:list):
        """Loads data from string file paths in a list and merge it into a single dictionary.
        """
        data = {}
        for file in file_path:
            _data = self._load_from_file(file)
            data.update(_data)
        return data

    @staticmethod
    def keyword_dot(data, keyword):
        """Return value in data for keyword.

        Returns value in nested dictionaries using dot separated keywords.
        """        
        for key in keyword.split(sep='.'):
            data = data[key]
        return data       
    
    def select(self, dict_name:str = None):
        """Selects dictionary from loaded file as default for
        Pathfinder.__getitem__() method.

        Parameters
        ----------
        dict_name : str, default None.
            Dictionary name to load as default.
            If None, returns to root dictionary.
            Select nested dictionaries using dot separated keywords.
        """
        if dict_name == None:
            self.data = self.original
        else:
            self.data = self.keyword_dot(self.original, dict_name)
        pass

    def get(self,keyword:str):
        """Return value assigned to keyword in loaded file.

        Ignores Pathfinder.select() directory.

        Parameters
        ----------
        keyword : str
            Dictionary keyword to look. Returns nested dictionaries 
            using dot separated keywords.
        """
        return self.keyword_dot(self.original, keyword)
