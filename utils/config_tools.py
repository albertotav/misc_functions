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
        If None, load configuration from ~/config/configuration.yml or .json.
    """

    def __init__(self, file_path:str = None):
        # Original data from file
        self.original = self._load_default(file_path)
        # Selected data (can be changed with methods)
        self.data = self.original

    def __getitem__(self, keyword:str):
        return self.keyword_dot(self.data, keyword)

    def _load_default(self, file_path):
        """Load configuration from ~/config/configuration.yml or .json if file_path == None.

        Returns loaded data from file_path.
        """
        if file_path == None:
            try:
                default_path = "config/configuration.yml"
                data = self._load_from_file(default_path)
            except FileNotFoundError:
                try:
                    default_path = "config/configuration.json"
                    data = self._load_from_file(default_path)
                except FileNotFoundError:                  
                    raise Exception("Could not find configuration.yml or .json in ~/config/")
        else:
            data = self._load_from_file(file_path)
        return data

    @staticmethod
    def read_json_file(file_path:str):
        """Read json file using yaml.SafeLoader.

        Returns parsed yml file.
        """
        # Get relative path from current working directory
        rel_path = os.path.relpath(file_path)
        parsed_yml = yaml.load(open(rel_path), Loader=yaml.SafeLoader)
        return parsed_yml

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
        """Load self.data from file_path.
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