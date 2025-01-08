from setuptools import setup, find_packages

setup(
    name='DATOE',
    version='0.1.0',
    description='A library to simplify eval and file handling in Telegram bots.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/DATOE',
    packages=find_packages(include=["*"]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
