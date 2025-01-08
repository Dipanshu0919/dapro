from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DATOE',
    version='0.1.0',
    description='A library to simplify eval and file handling in Telegram bots.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dipanshu',
    author_email='dipanshu0919@gmail.com',
    url='https://github.com/Dipanshu0919/DATOE',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3.0 (GPL-3.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='GPL-3.0',
)