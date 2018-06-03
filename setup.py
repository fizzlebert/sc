import setuptools

setuptools.setup(
    name="sc",
    version="0.0.1",
    author="Daniel O'Connell",
    author_email="dan.ben.oconnell@gmail.com",
    description="Download songs from SoundCloud.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danieloconell/sc",
    packages=setuptools.find_packages(),
    install_requires=open("requirements.txt").read().split("\n"),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["sc= sc.sc:main"]},
)
