import os

from setuptools import setup


def fread(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as f:
        return f.read()


setup(name='Flask-SlackBot',
      version='0.0.6',
      url='https://github.com/python-cn/flask-slackbot',
      license='MIT',
      author='halfcrazy',
      author_email='hackzhuyan@gmail.com',
      description='Deal with slack outgoing webhook ',
      long_description=fread('README.rst'),
      py_modules=['flask_slackbot'],
      zip_safe=False,
      platforms='any',
      install_requires=[
          'Flask',
          'slacker',
          'six'
      ],
      tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])
