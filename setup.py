from setuptools import setup, find_packages

setup(
    name='cbz_editor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rich',
        'rich-click'
    ],
    entry_points={
        'console_scripts': [
            'cbz-editor=cbz_editor.cli:cli',
        ],
    },
    extra_requirements={
        'dev': [
            'pyinstaller',
        ],
    },
    author='Schmidti',
    description='A CBZ editor for processing and renaming comic files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SchmidtiTv/cbz_editor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    python_requires='>=3.6',
)
