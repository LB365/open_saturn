from setuptools import setup

REQUIREMENTS = [
    'dw_squared @ git+https://github.com/lofriedman/dw-squared.git@master',
    'tsview',
    'tshistory==0.14.1',
    'rework',
    'tshistory_refinery',
    'tshistory_editor',
    'tshistory_xl',
    'tshistory_rest',
    'tshistory_formula',
    'flask<2.0',
    'flask-oidc>=1.4.0',
    'okta==0.0.4',
    'pandas',
    'mock',
    'inireader',
    'apscheduler',
    'gunicorn',
    'psycopg2-binary',
]

setup(
    name='open_saturn',
    version='1.0',
    packages=['open_saturn'],
    package_dir={
        'open_saturn': 'open_saturn'
    },
    package_data={'open_saturn': [
        'templates/*'
    ]},
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'saturn=open_saturn.cli:saturn',
        ],
    },
)
