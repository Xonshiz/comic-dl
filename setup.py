import setuptools

from comic_dl import __version__

setuptools.setup(
    name='comic_dl',
    version=__version__.__version__,
    description='Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.',
    long_description='Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.',
    author='Xonshiz',
    author_email='xonshiz@gmail.com',
    url='https://github.com/Xonshiz/comic-dl',
    packages=setuptools.find_packages(),
    keywords=['comic-dl', 'cli', 'comic downloader', 'manga downloader', 'mangafox', 'batoto', 'kissmanga',
              'comic naver', 'readcomiconline'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics'
    ],
    entry_points={"console_scripts": ["comic_dl=comic_dl.__main__:main"]}
)
