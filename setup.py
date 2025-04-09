import setuptools


setuptools.setup(
    name='left',
    version='0.0.6',
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
    install_requires=["flet[all]==0.27.6", "dataclasses_json==0.6.3",
                      "tinydb==4.8.2", "tinyrecord==0.2.0"],
    include_package_data=True
)
