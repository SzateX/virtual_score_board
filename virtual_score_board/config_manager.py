import sys
from configparser import ConfigParser
from configparser import NoOptionError


class ConfigManager(object):
    default_config = {
        "interface": "0.0.0.0",
        "port": 9000
    }
    config_path = ""

    def read_config(self):
        config = ConfigParser()
        readed_files = config.read(self.config_path)
        if len(readed_files) == 0:
            sys.stderr.write("Error! I can't read config file (Propably not exists)! Loaded default config! \n")
            return
        for key in self.default_config:
            try:
                setattr(self, key, config.get('AppConfig', key)
            except NoOptionError:
                sys.stderr.write("[AppConfig].%s doesn't exist. Loaded default value! \n" % key)
                setattr(self, key, self.default_config[key])