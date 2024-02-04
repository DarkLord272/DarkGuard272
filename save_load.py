import configparser
CONFIG_FILE = 'darkguard_config.ini'

def save_config(key, value):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config['Settings'][key] = value
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

def load_config(key):
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE)
        if 'Settings' in config and key in config['Settings']:
            return config['Settings'][key]
    except Exception as e:
        print(f"Error loading config: {e}")
    return 'Default1' if key == 'Theme' else 'False' if key == 'AutoUpdate' else 'False'