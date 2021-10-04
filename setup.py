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
    package_data={'open_saturn': [
        'templates/*'
    ]},
    install_requires=[
        'Flask',
        'pandas >= 1.0',
        'mock',
        'inireader',
        'apscheduler',
        'tshistory_editor @ https://hg.sr.ht/~pythonian/tshistory_editor/archive/0.8.2.tar.gz#egg=tshistory_editor',
        'tshistory_rest @ https://hg.sr.ht/~pythonian/tshistory_rest/archive/0.10.0.tar.gz#egg=tshistory_rest',
        'tshistory_refinery @ https://hg.sr.ht/~pythonian/tshistory_refinery/archive/0.2.0.tar.gz#egg=tshistory_refinery',
    ],
    entry_points={
        'tshistory.subcommands': [
            'openwebstart=open_saturn.cli:openwebstart',

        ],
    },
    extras_require={'heroku': ["gunicorn", "psycopg2"]},
)
