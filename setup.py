from setuptools import setup

setup(name='fints-url',
      version='0.2',
      description='FinTS URL Retriever',
      long_description='FinTS URL Retriever is a web scraper which tries to retrieve the FinTS URL of german banks.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Accounting',
      ],
      keywords='fints url bank german iban code',
      url='http://github.com/dr-duplo/python-fints-url',
      author='dr-duplo',
      author_email='monsieur.cm@gmx.de',
      license='MIT',
      packages=['fints_url'],
      install_requires=[
          'requests', 'lxml', 'schwifty', 'argparse'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose', 'mock', 'argparse'],
      entry_points = {
        'console_scripts': ['fints-url=fints_url.cli:main'],
        })
