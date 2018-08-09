from distutils.core import setup

readme = open('ReadMe.md').read()
history = open('Changelog.md').read()

setup(
  name = 'comic_dl',
  packages = ['comic_dl','comic_dl.sites', 'comic_dl.manga_eden'], # this must be the same as the name above
  install_requires=["selenium",
                    "requests",
                    "more_itertools",
                    "cfscrape",
                    "bs4",
                    "clint",
                    "enum34",
                    "future",
                    "img2pdf",
                    "more_itertools",
                    "tqdm",
    ],
  version = '2018.01.10',
  description = 'Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.',
  long_description=readme + '\n\n' + history,
  author = 'Xonshiz',
  author_email = 'xonshiz@psychoticelites.com',
  url='https://github.com/Xonshiz/comic-dl',
  download_url = 'https://codeload.github.com/Xonshiz/comic-dl/tar.gz/2018.1.10',
  keywords = ['comic-dl', 'cli', 'comic downloader','manga downloader','mangafox','batoto','kissmanga','comic naver','readcomiconline'],
  classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics'
    ],
)
