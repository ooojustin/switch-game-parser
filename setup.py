from distutils.core import setup

setup(name='switch-game-parser',
      version='0.1',
      description='Programatically parsing Nintendo Switch games',
      author='Justin Garofolo',
      author_email='justin@garofolo.net',
      url='https://github.com/ooojustin/switch-game-parser',
      license='MIT',
      packages=['switch-game-parser'],
      install_requires=[
        'sphinx'
        'sphinx_bootstrap_theme',
        'requests',
        'mysql_connector'
        ]
     )
