from setuptools import setup

versions = {
    'tshistory': '0.13.0',
    'tshistory_editor': '0.8.2',
    'tshistory_rest': '0.10.0',
    'tshistory_refinery': '0.2.0',
    'tshistory_xl': '0.2.1',
}


def hgsr_repo(repo_name, version):
    return f'{repo_name} @ https://hg.sr.ht/~pythonian' / \
           f'{repo_name}/archive/{version}.tar.gz#egg={repo_name}'


_REQUIREMENTS = [
    'pandas<1.2',
    'mock',
    'inireader',
    'apscheduler',
]

SATURN_REQUIREMENTS = [hgsr_repo(k, v) for k, v in versions.items()]

REQUIREMENTS = _REQUIREMENTS + SATURN_REQUIREMENTS[:-1]

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
        'tshistory.subcommands': [
            'openwebstart=open_saturn.cli:openwebstart',

        ],
    },
    extras_require={
        'remote': [
            'gunicorn',
            'psycopg2-binary'
        ],
        'xl': [
            'xlwings',
            SATURN_REQUIREMENTS[-1],
        ]},
)
