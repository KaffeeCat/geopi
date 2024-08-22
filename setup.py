import setuptools

setuptools.setup(
    name="geopi",
    version="0.1.8",
    author="Wang Kang",
    author_email="prince.love@live.cn",
    description="面向中国的时空位置数据处理工具包",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        requirement for requirement in open('requirements.txt').readlines()
        if requirement.strip() and not requirement.startswith('-')
    ],
    package_data={
        'geopi': ['data/*.json', 'data/city_boundary/*.json', 'data/city_shp/*.zip'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
