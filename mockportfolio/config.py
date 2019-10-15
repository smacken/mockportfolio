''' configuration '''
from os.path import expanduser, join
import yaml

DEFAULT_CONFIG = {
    'title': 'Mock Portfolio'
}


class ConfigLoader(object):
    ''' configuration '''

    CONFIG_FILE_NAME = '.mockportfolio.yaml'

    def __init__(self):
        self.__dict__.update(DEFAULT_CONFIG)

    @property
    def abs_path(self):
        ''' absolute file path '''
        return join(
            expanduser("~"),
            self.CONFIG_FILE_NAME
        )

    def load(self):
        ''' load config '''
        try:
            config_content = open(self.abs_path, 'rb').read()
            self.__dict__.update(yaml.load(config_content))
        except IOError as exc:
            print(exc)
        return self


config = ConfigLoader().load()
