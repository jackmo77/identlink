from setuptools import setup, find_packages

setup(name='hgame-ident',
      version='0.1',
      packages=['hgame.ident'],
      install_package_data=True,
      install_requires=[
          'click', 'pandas', 'tabulate'
      ],
      entry_points="""
         [console_scripts]
         hgame-ident=hgame.ident.main:cli
      """
      )
