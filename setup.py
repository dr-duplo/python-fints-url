from setuptools import setup
import setuptools.command.build_py
import sys, os

sys.path.append(os.path.dirname(__file__))
from fints_url import update_bank_info

class UpdateBankInfoCommand(setuptools.command.build_py.build_py):
  """Update Bank Info."""

  def run(self):
    update_bank_info.update()


class BuildPyCommand(setuptools.command.build_py.build_py):
  """Update bank info for every build."""

  def run(self):
    self.run_command('update_bank_info')
    setuptools.command.build_py.build_py.run(self)

setup(name='fints-url',
      version='0.7',
      description='FinTS URL Retriever',
      long_description='FinTS URL Retriever is a small library to retrieve the FinTS URLs of german banks.',
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
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose', 'mock', 'argparse'],
      entry_points = {
        'console_scripts': ['fints-url=fints_url.cli:main'],
        },
      cmdclass={
        'update_bank_info' : UpdateBankInfoCommand,
        'build_py': BuildPyCommand
      })
