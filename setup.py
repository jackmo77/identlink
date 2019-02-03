from setuptools import setup, find_packages

setup(name='identlink',
      version='0.1',
      packages=find_packages(),
      install_package_data=True,
      install_requires=[
          'pathlib2', 'click', 'pandas', 'tabulate'
      ],
      entry_points="""
         [console_scripts]
         identlink=identlink.main:cli
      """
      )
