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
        if file_path == None:
            try:
                self.file_path = "config/configuration.yml"
                self.data = self._load_from_file(self.file_path)
            except FileNotFoundError:
                try:
                    self.file_path = "config/configuration.json"
                    self.data = self._load_from_file(self.file_path)
                except FileNotFoundError:                  
                    raise Exception("Could not find configuration.yml or .json in ~/config/")
        else:
            self.file_path = file_path
            self.data = self._load_from_file(self.file_path)
            pass

    def __getitem__(self, keyword:str):
        return self._get(keyword)

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
            self.data = self._load_from_file(self.file_path)
        else:
            temp_data = self.data
            for key in dict_name.split(sep='.'):
                temp_data = temp_data[key]
        self.data = temp_data
        pass

    def _get(self,keyword:str):
        """Return value assigned to keyword in loaded file.
        
        Uses default dictionary selected by Pathfinder.select() method.

        Parameters
        ----------
        keyword : str
            Dictionary keyword to look. Returns nested dictionaries 
            using dot separated keywords.
        """
        temp_data = self.data
        for key in keyword.split(sep='.'):
            temp_data = temp_data[key]
        return temp_data

    def get(self,keyword:str):
        """Return value assigned to keyword in loaded file.

        Ignores Pathfinder.select() default directory.

        Parameters
        ----------
        keyword : str
            Dictionary keyword to look. Returns nested dictionaries 
            using dot separated keywords.
        """
        temp_data = self._load_from_file(self.file_path)

        for key in keyword.split(sep='.'):
            temp_data = temp_data[key]
        return temp_data