import codecs
from setuptools import setup, find_packages

setup(
    name='etimedecorator',
    version='1.0.1',
    description='eTimeDecorator is a set of 3 elapsed timer decorators for Python 3.x and PyPy3 to measure the execution time of a function that executes hundreds/thousands of times per second. It also works with asyncio. Records the minimum, average and maximum elapsed time of functions and calculates the percentile.',
    url='https://github.com/rabuchaim/etimedecorator',
    author='Ricardo Abuchaim',
    author_email='ricardoabuchaim@gmail.com',
    maintainer='Ricardo Abuchaim',
    maintainer_email='ricardoabuchaim@gmail.com',
    project_urls={
        "Issue Tracker": "https://github.com/rabuchaim/etimedecorator/issues",
        "Source code": "https://github.com/rabuchaim/etimedecorator",
    },    
    bugtrack_url='https://github.com/rabuchaim/etimedecorator/issues',    
    license='MIT',
    keywords=['elapsed','elapsed timer','elapsedtimer','elapsedtime','elapsed time','timer','perf_counter','monotonic','timeit','timing','decorator','debug','performance'],
    packages=find_packages(),
    py_modules=['etimedecorator', 'etimedecorator'],
    package_dir = {'etimedecorator': 'etimedecorator'},
    include_package_data=True,
    zip_safe = False,
    package_data={
        'etimedecorator': [
            'CHANGELOG.md', 
            'README.md',
            'LICENSE',
            'etimedecorator/__init__.py'
            'etimedecorator/etimedecorator.py'
            'etimedecorator/test_etimedecorator.py'
        ],
    },
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Security',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',  
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
    ],
    long_description=codecs.open("README.md","r","utf-8").read(),
    long_description_content_type='text/markdown',
)
