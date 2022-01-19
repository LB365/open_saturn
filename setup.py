from setuptools import setup

versions = {
    # 'tshistory': '0.14.0',
    # 'tshistory_editor': '0.8.2',
    # 'tshistory_rest': '0.10.0',
    # 'tshistory_refinery': '0.3.0',
    # 'tshistory_xl': '0.3.0',
    # 'tshistory_formula': '0.10.0',
    # 'rework': '0.14.0',
    # 'tsview': '0.13.0',
}



def hgsr_repo(repo_name, version):
    return f'{repo_name} @ https://hg.sr.ht/~pythonian/' \
           f'{repo_name}/archive/{version}.tar.gz#egg={repo_name}'


_REQUIREMENTS = [
    'tshistory',
    'rework',
    'tsview @ git+https://github.com/lofriedman/tsview.git@master#egg=tsview',
    'tshistory_refinery',
    'tshistory_editor',
    'tshistory_xl',
    'tshistory_rest',
    'tshistory_formula',
    'flask<2.0',
    'flask-oidc>=1.4.0',
    'okta==0.0.4',
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
