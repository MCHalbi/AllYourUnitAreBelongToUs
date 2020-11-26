import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pythonunits-MCHalbi',
    version='0.0.1',
    author='Lukas Halbritter',
    author_email='halbi93@gmx.de',
    description='A package for units.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MCHalbi/PythonUnits',
    packages=setuptools.find_packages(),
    classfiers=[
        'Development Status :: 1 - Planning'
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
