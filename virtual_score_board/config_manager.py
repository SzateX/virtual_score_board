import sys
from configparser import ConfigParser
from configparser import NoOptionError


class ConfigManager(object):
    default_config = {
        "host": "0.0.0.0",
        "port": 5000,
        "use_ssl": False,
        "append_port_to_url": False,
        "log_file_path": "log.txt"
    }
    config_path = "config.ini"

    def read_config(self):
        config = ConfigParser()
        read_files = config.read(self.config_path)
        if len(read_files) == 0:
            sys.stderr.write("Error! I can't read config file (Probably not exists)! Loaded default config! \n")
            return
        for key in self.default_config:
            try:
                setattr(self, key, config.get('AppConfig', key))
            except NoOptionError:
                sys.stderr.write("[AppConfig].%s doesn't exist. Loaded default value! \n" % key)
                setattr(self, key, self.default_config[key])
