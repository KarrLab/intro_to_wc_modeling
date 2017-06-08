from setuptools import setup, find_packages
import karr_lab_tutorials

# parse dependencies from requirements.txt files
install_requires = []
tests_require = []

for line in open('requirements.txt'):
    line, _, _ = line.partition('#')
    line = line.strip()
    install_requires.append(line)

for line in open('tests/requirements.txt'):
    line, _, _ = line.partition('#')
    line = line.strip()
    tests_require.append(line)

# install package
setup(
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
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'karr_lab_tutorials = karr_lab_tutorials.__main__:main',
        ],
    },

    install_requires=install_requires,
    tests_require=tests_require,
    dependency_links=[],
)
