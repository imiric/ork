from setuptools import setup

from ork import get_version

setup(
    name='ork',
    version=get_version(),
    url='http://github.com/imiric/ork/',
    description='A distributed task orchestrator',
    author='Ivan Mirić',
    author_email='imiric@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Distributed Computing',
    ],
    packages=['ork'],
    install_requires=[
        'click==6.3'
    ],
    entry_points={'console_scripts': ['ork = ork.cli:cli']},
)
