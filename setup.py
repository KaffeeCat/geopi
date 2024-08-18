import setuptools

setuptools.setup(
    name="geopi",
    version="0.1.2",
    author="author",
    author_email="author@example.com",
    description="A small example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        requirement for requirement in open('requirements.txt').readlines()
        if requirement.strip() and not requirement.startswith('-')
    ],
    package_data={
        'geopi': ['data/*.json', 'data/city_boundary/*.json', 'data/city_shp/*.*'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
