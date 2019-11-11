import setuptools
from src.akitools import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="akitools",
    version=__version__,
    author="aki",
    author_email="heti@qq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="akitools",
    url="https://github.com/aki/akitools",
    py_modules  = ['akitools'],
    package_dir = {'': 'src'},
    license = 'BSD',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'python-dateutil>=2.8.0'
    ]
)
