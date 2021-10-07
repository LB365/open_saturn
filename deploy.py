from configparser import ConfigParser
import os


def replace_uri(refinery_file):
    config = ConfigParser()
    config.read(refinery_file)
    if 'DATABASE_URL' in os.environ.keys() is not None:
        prefix = 'postgres'
        url = os.environ['DATABASE_URL'].replace(prefix, prefix + 'ql')
        if not config.get('db', 'uri').startswith('postgresql'):
            config.set('db', 'uri', url)
    with open(refinery_file, 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    REFINERY_FILE = 'refinery.ini'
    replace_uri(REFINERY_FILE)
