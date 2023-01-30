from setuptools import setup, find_namespace_packages


setup(
    name='clean_folder',
    version='1',
    description='Rename files and directories, sort files, delete empty directories in specified folder',
    url='https://github.com/DenysKotsiuba/homework_2',
    author='Denys Kotsiuba',
    author_email='denis.kotsiuba@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:clean_folder']},
)