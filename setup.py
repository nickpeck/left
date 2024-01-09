import setuptools


setuptools.setup(
    name='drybones',
    version='0.0.1',
    license='LICENSE',
    author='nickpeck',
    author_email='',
    description='A bare-bones CRUD framework for single-page apps built upon python flet',
    keywords=['flet', 'framework', 'crud'],
    url='',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.10',
    include_package_data=True,
)