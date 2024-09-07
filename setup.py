from setuptools import setup

setup(
    name='cbz_editor',
    version='0.1',
    py_modules=['cbz_editor'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        cbz_editor=cbz_editor:cli
    ''',
    author='Schmidti',
    description='A CBZ editor for processing and renaming comic files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cbz_editor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
