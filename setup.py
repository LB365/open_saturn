from setuptools import setup
import os
import platform

if platform.system() == 'Linux':
    os.environ["INSTALL_ON_LINUX"] = "1"

setup(
    name='open_saturn',
    version='1.0',
    packages=['pm_utils', 'open_saturn'],
    package_dir={'pm_utils': 'pm_utils', 'open_saturn': 'open_saturn'},
    install_requires=[
        'gunicorn',
        'psycopg2',
        'flask<2.0',
        'tshistory_refinery @ https://hg.sr.ht/~pythonian/tshistory_refinery/archive/0.2.0.tar.gz#egg=tshistory_refinery',
        'tzlocal~=2.0',
        'werkzeug',
        'mock',
        'inireader',
        'xlwings',
        'apscheduler',
    ],
    entry_points={
        'tshistory.subcommands': [
            'openwebstart=open_saturn.cli:openwebstart',

        ],
    }
)
