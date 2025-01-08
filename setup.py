from setuptools import setup, find_packages

setup(
    name='DATOE',
    version='0.1.0',
    description='A library to simplify eval and file handling in Telegram bots.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dipanshu',
    author_email='dipanshu0919@gmail.com',
    url='https://github.com/Dipanshu0919/DATOE',
    packages=find_packages(include=["*"]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
