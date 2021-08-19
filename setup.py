import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='unitpy',
    version='0.0.1',
    url='https://github.com/dylanwal/unitpy',
    author='Dylan',
    author_email='',
    description='Unit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "unitpy"},
    packages=setuptools.find_packages(where="unitpy"),
    python_requires=">=3.6",
)