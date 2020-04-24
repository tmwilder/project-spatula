#!/usr/bin/env python

from distutils.core import setup

setup(name='spatula',
      version='1.0',
      description='Get those crads',
      author='Tim Wilder',
      author_email='tmwilder@gmail.com',
      url='https://www.mtgshuffle.com',
      requires=[
            'requests',
            "beautifulsoup4",
            "alembic",
            "sqlalchemy",
            "mysqlclient",
            "flask"],
      packages=['spatula'])
