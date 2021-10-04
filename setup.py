from setuptools import setup

with open('requirements.txt', 'rb') as f:
    lines = f.readlines()

setup(name='open_saturn',
      version='2.0',
      packages=['pm_utils', 'open_saturn'],
      package_dir={'pm_utils': 'pm_utils', 'open_saturn': 'open_saturn'},
      install_requires=[
          'gunicorn',
          'psycopg2',
          'flask<2.0',
          'tzlocal~=2.0',
          'xlwings',
          'rework',
          'rework_ui',
          'tsview',
          'tshistory',
          'tshistory_client',
          'tshistory_rest',
          'tshistory_formula',
          'tshistory_editor',
          'tshistory_refinery',
          'tshistory_xl',
          'werkzeug',
          'mock',
          'apscheduler',
      ]
      )
