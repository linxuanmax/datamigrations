#!/opt/secsphere/bin/python
# -*- coding: utf-8 -*-

import os
import stat
import codecs
from glob import glob

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


import datamigrations

packages, data_files = [], []
root_dir = os.path.dirname(__file__)

if root_dir != '':
    os.chdir(root_dir)

if os.path.exists("README"):
    long_description = codecs.open('README', "r", "utf-8").read()
else:
    long_description = ""

src_dir = "datamigrations"

conf_target = '/opt/datamigrations/conf/datamigrations'
conf_file = filter(os.path.isfile, glob(src_dir + '/conf/*.conf'))

additional_files = [(conf_target, conf_file)]

setup(
	name = "datamigrations",
	version=datamigrations.__version__,
	description=datamigrations.__doc__,
	author=datamigrations.__author__,
	author_email=datamigrations.__contact__,
	url=datamigrations.__homepage__,
	platforms=["any"],
	packages=find_packages(),
	data_files=additional_files,
	zip_safe=False,
	scripts=["bin/run.py"],
	classifiers=[
	"Development Status :: 2 - Alpha",
	"Operating System :: OS Independent",
	"Programming Language :: Python",
	"License :: OSI Approved :: GPL License",
	"Intended Audience :: Developers",
	],
	long_description=long_description,
)


if os.path.exists(conf_target + '/datamigrations.conf'):
    os.chmod(conf_target + '/datamigrations.conf', stat.S_IWRITE|stat.S_IREAD|stat.S_IWGRP|stat.S_IRGRP|stat.S_IWOTH|stat.S_IROTH)



