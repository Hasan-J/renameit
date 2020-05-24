import codecs
from setuptools import setup


VERSION = '0.1.0'

def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()


setup(
    name='renameit',
    packages=['renameit'],
    version=VERSION,
    description='File renaming tool.',
    long_description=read_file('README.md'),
    license='MIT',
    author='Hasan Jawad',
    author_email='hasan_sg@hotmail.com',
    url='https://github.com/Hasan-J/renameit',
    keywords=[
        'renameit', 'change', 'files', 'renaming', 'naming files',
        'refactor', 'rename', 'file names'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)