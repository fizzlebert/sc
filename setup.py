from sc.__version__ import __author__, __author_email__, __title__, __version__

import setuptools

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description="Download songs from SoundCloud.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danieloconell/sc",
    packages=["sc"],
    install_requires=["mutagen", "requests", "docopt", "tqdm"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["sc= sc.sc:main"]},
)
