import configparser
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_dir, 'config.ini')

props = configparser.ConfigParser()
props.read(config_path, encoding='UTF-8')
DEFAULT = props['DEFAULT']
print(DEFAULT['api_key'])