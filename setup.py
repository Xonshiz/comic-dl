import setuptools

from comic_dl import __version__

readme = open('ReadMe.md').read()
history = open('Changelog.md').read()

setuptools.setup(
    name="comic_dl", # Replace with your own username
    version=__version__.__version__,
    author="Xonshiz",
    author_email='xonshiz@gmail.com',
    url='https://github.com/Xonshiz/comic-dl',
    download_url='https://github.com/Xonshiz/comic-dl/releases/latest',
    description="Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.",
    long_description='{0}\n\n{1}'.format(readme, history),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)

