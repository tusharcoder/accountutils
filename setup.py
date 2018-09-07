# @Author: Tushar(tusharcoder) <tushar>
# @Date:   05/09/18
# @Email:  tamyworld@gmail.com
# @Filename: setup
# @Last modified by:   Tushar

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-accountutils',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A django app for basic utilities - user registration, login, change password, reset password',
    long_description=README,
    url='https://github.com/tusharcoder/accountutils',
    author='Tushar Agarwal',
    author_email='tamyworld@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)