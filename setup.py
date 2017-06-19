import pip
pip.main(['install', 'git+https://github.com/KarrLab/wc_utils.git#egg=wc_utils'])

import karr_lab_tutorials
import os
import setuptools
import wc_utils.util.install

# parse dependencies and links from requirements.txt files
with open('requirements.txt', 'r') as file:
    install_requires, dependency_links_install = wc_utils.util.install.parse_requirements(file.readlines())
with open('tests/requirements.txt', 'r') as file:
    tests_require, dependency_links_tests = wc_utils.util.install.parse_requirements(file.readlines())
dependency_links = list(set(dependency_links_install + dependency_links_tests))

# install non-PyPI dependencies
wc_utils.util.install.install_dependencies(dependency_links)


# install package
setuptools.setup(
    name='karr_lab_tutorials',
    version=karr_lab_tutorials.__version__,

    description='Python tutorial',

    # The project's main homepage.
    url='https://github.com/KarrLab/karr_lab_tutorials',

    author='Jonathan Karr',
    author_email='jonrkarr@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],

    keywords='python, tutorial',

    # packages not prepared yet
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    package_data={
        'karr_lab_tutorials': [
            os.path.join('wc_modeling', 'wc_lang_tutorial', 'examples', 'test_wc_lang.xlsx')
        ],
    },
    entry_points={
        'console_scripts': [
            'karr_lab_tutorials = karr_lab_tutorials.__main__:main',
        ],
    },

    install_requires=install_requires,
    tests_require=tests_require,
    dependency_links=dependency_links,
)
