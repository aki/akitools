import setuptools
from src.__init__ import __version__

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
    packages=['akitools'],
    package_dir={'akitools': 'src'},
    license='BSD',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ]
)
