import os
import yaml
from settings import *

class Friend:
    def __init__(self, **kwargs):
        self.name = ''
        self.photos = []
        self.friends = set() # stores the slug name
        for k, v in kwargs.items():
            setattr(self, k, v)
    @staticmethod
    def _get_yaml_path(name: str):
        return os.path.join(APP_BASE, DATA_PREFIX, f"{Friend.get_slug(name)}.yaml")
    @staticmethod
    def get_slug(name: str):
        return name.lower().replace(' ', '-')
    @property
    def slug(self):
        return Friend.get_slug(self.name)
    @staticmethod
    def load(name: str):
        yaml_path = Friend._get_yaml_path(name)
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as data_file:
                try:
                    person = yaml.load(data_file, yaml.Loader)
                    return person
                except Exception:
                    # Malformed yaml! Remove it
                    os.remove(yaml_path)
        return None
    def save(self):
        yaml_path = Friend._get_yaml_path(self.name)
        try:
            f = open(yaml_path, 'r+')
        except FileNotFoundError:
            f = open(yaml_path, 'w')
        finally:
            yaml.dump(self, f)
            f.close()

class Photo:
    def __init__(self, fp, exif = None):
        self.fp = fp
        self.exif = exif
