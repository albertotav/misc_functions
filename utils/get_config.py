import os
import json
import yaml

class Config_loader:
    """Tool for loading configuration files in .yml or .json

    Designed for using a json or yml file as "path library", getting
    the desired value with Config_loader.get(Keyword) or Config_loader[Keyword].

    Can return multiple nested dictionaries/lists.
    """

    def __init__(self, file_path:str):
        self.file_path = file_path
        self._load_from_file(self.file_path)
        pass

    def __getitem__(self, keyword:str):
        return self.get(keyword)

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

    def _load_from_file(self, file_path:int):
        """Load self.data from file_path
        """
        # Get file format from string
        file_format = file_path.split(sep='.')[-1]

        if file_format == 'yml' or file_format == 'yaml':
            self.data = self.read_yml_file(file_path)

        elif file_format == 'json':
            self.data = self.read_json_file(file_path)        
        else:
            raise Exception("Wrong file format. Use yml/yaml or json files")
        pass

    def get_dict(self):
        """Returns default dictionary.
        """
        return self.data
    
    def select(self, dict_name:str):
        """Selects dictionary from loaded file as default for
        Config_loader.get() method.

        dict_name : string
            Dictionary name to load as default.
            If None, returns to root dictionary.
        """
        if dict_name == None:
             self._load_from_file(self.file_path)
        else:
            self.data = self.data[dict_name]
        pass

    def get(self,keyword:str, nested_dict:str = None):
        """Return value assigned to keyword in loaded file.
        
        Change default dictionary using Config_loader.select() method.

        Parameters
        ----------
        keyword : string
            Dictionary keyword to look

        nested_dict : string
            Select a nested dictionary in default dictionary to search for keyword.
        """
        if nested_dict == None:
            return self.data[keyword]
        else:
            return self.data[nested_dict][keyword]   