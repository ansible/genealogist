from setuptools import find_packages, setup

setup(
    name='Ansible Geneology',
    version='1.0',
    install_requires=[
        'Click',
        'GitPython',
        'PyYAML'
    ],
    include_package_data=True,
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        genealogist=genealogist.genealogist:cli
    '''
)
