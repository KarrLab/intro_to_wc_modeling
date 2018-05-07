import setuptools
try:
    import pkg_utils
except ImportError:
    import pip._internal
    pip._internal.main(['install', '--process-dependency-links', 'git+https://github.com/KarrLab/pkg_utils.git#egg=pkg_utils'])
    import pkg_utils
import os

name = 'intro_to_wc_modeling'
dirname = os.path.dirname(__file__)

# get package metadata
md = pkg_utils.get_package_metadata(dirname, name)

# install package
setuptools.setup(
    name=name,
    version=md.version,

    description='An introduction to whole-cell modeling',
    long_description=md.long_description,

    # The project's main homepage.
    url='https://github.com/KarrLab/' + name,
    download_url='https://github.com/KarrLab/' + name,

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
    package_data={
        name: [
            'VERSION',
            os.path.join('wc_modeling', 'wc_lang_tutorial', 'examples', 'test_wc_lang.xlsx'),
        ],
    },
    entry_points={
        'console_scripts': [
            'intro_to_wc_modeling = intro_to_wc_modeling.__main__:main',
        ],
    },

    install_requires=md.install_requires,
    extras_require=md.extras_require,
    tests_require=md.tests_require,
    dependency_links=md.dependency_links,
)
