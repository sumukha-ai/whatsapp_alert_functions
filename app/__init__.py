import configparser
import logging
import os
import pathlib

from flask import Flask




app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:[%(levelname)s] %(filename)s: %(funcName)s: %(lineno)d - %(message)s')  # Set the logging level here

# Alternatively, configure Flask's logger directly
app.logger.setLevel(logging.DEBUG)

def set_env_vars_from_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            # Ignore lines starting with '#' (comments) or empty lines
            if line.strip() and not line.strip().startswith('#'):
                # Split each line into variable name and value
                var_name, var_value = line.strip().split('=', 1)
                # Set the environment variable
                os.environ[var_name] = var_value


file_name = os.getenv("ENV_FILE")
print("*************", file_name)
logging.getLogger().info(file_name)
set_env_vars_from_file(file_name)

class EnvConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # override the ConfigParser.get method to always take os.environ as vars.
    def get(self, section, option, *, raw=False, vars=os.environ, fallback=configparser._UNSET):
        return super().get(section, option, raw=raw, vars=vars, fallback=fallback)



config = EnvConfigParser()
# Load configurations from config.ini file
config_path = pathlib.Path(__file__).parent.absolute() / "config/config.ini"
config.read(config_path)

# Configure SQLAlchemy





from .routes.webhook import webhook_bp
app.register_blueprint(webhook_bp)


