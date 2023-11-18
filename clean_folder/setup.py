from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_xxx',
    version='0.0.1',
    description='GOIT. clean folder',
    author='Mykhailo Murat',
    author_email='mykhailo.murat@gmail.com',
    license='MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['cleanfolder=clean_folder.main:start']}
)