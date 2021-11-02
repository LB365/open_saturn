from setuptools import setup

versions = {
    'tshistory': '0.13.0',
    'tshistory_editor': '0.8.2',
    'tshistory_rest': '0.10.0',
    'tshistory_refinery': '0.2.0',
    'tshistory_xl': '0.2.1',
}


def hgsr_repo(repo_name, version):
    return f'{repo_name} @ https://hg.sr.ht/~pythonian/' \
           f'{repo_name}/archive/{version}.tar.gz#egg={repo_name}'


_REQUIREMENTS = [
    'flask<2.0',
    'flask-oidc @ git+https://github.com/puiterwijk/flask-oidc/archive/master.zip',
    'okta',
    'pandas<1.2',
    'mock',
    'inireader',
    'apscheduler',
    'gunicorn',
    'psycopg2-binary',
]

SATURN_REQUIREMENTS = [hgsr_repo(k, v) for k, v in versions.items()]

REQUIREMENTS = _REQUIREMENTS + SATURN_REQUIREMENTS

setup(
    name='open_saturn',
    version='1.0',
    packages=['pm_utils', 'open_saturn'],
    package_dir={
        'pm_utils': 'pm_utils',
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
