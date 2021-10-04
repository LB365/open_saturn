from setuptools import setup

setup(
    name='open_saturn',
    version='2.0',
    packages=['pm_utils', 'open_saturn'],
    package_dir={'pm_utils': 'pm_utils', 'open_saturn': 'open_saturn'},
    install_requires=[
        'gunicorn',
        'psycopg2',
        'flask<2.0',
        'tzlocal~=2.0',
        'werkzeug',
        'mock',
        'apscheduler',
    ],
    entry_points={
        'tshistory.subcommands': [
            'openwebstart=open_saturn.cli:openwebstart',

        ],
    }
)
