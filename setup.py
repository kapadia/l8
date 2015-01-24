from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    'click',
    'boto',
    'rasterio>=0.15.1',
    'pyproj>=1.9.3',
    'matplotlib>=1.4.0',
    'seaborn>=0.5.0'
]

setup(name='l8',
      version='0.0.1',
      description=u"Collection of routines for working with Landsat 8 imagery.",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Amit Kapadia",
      author_email='amit@mapbox.com',
      url='https://github.com/kapadia/l8',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      l8=l8.scripts.cli:l8
      """
      )
