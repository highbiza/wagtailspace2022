from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    # package name in pypi
    name='wagtailspace2022',
    # extract version from module.
    version=__version__,
    description="Roadrunner demo site for wagtailspace2022",
    long_description="Roadrunner demo site",
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # for avoiding conflict have one namespace for all apc related eggs.
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'wagtail<3.0',
        'django<4',
        'wagtail-roadrunner@git+https://github.com/highbiza/wagtail-roadrunner.git#egg=wagtail-roadrunner'
    ],
    dependency_links=['git+https://github.com/highbiza/wagtail-roadrunner.git#egg=wagtail-roadrunner']
)
