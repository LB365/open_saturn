from setuptools import setup

with open('requirements.txt', 'rb') as f:
    lines = f.readlines()

setup(name='pm_utils',
      version='2.0',
      packages=['pm_utils'],
      package_dir={'pm_utils': 'pm_utils', 'open_saturn': 'open_saturn'},
      install_requires=[
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
