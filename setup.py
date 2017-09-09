from setuptools import setup

VERSION = '0.2.0'

setup(name='yld',
      version=VERSION,
      author='Gabriel Lima',
      author_email='gvclima@gmail.com',
      description='Deployment helper',
      license='MIT',
      keywords='deployment',
      url='https://github.com/ewilazarus/yld',
      packages=['yld'],
      install_requires=[
          'click==6.7'
      ],
      entry_points={
          'console_scripts': ['yld=yld.__main__:main']
      })
