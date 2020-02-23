import io
from setuptools import find_packages, setup

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name="challenge",
    description="solution of a DS coding task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # include_package_data=True,
    # zip_safe=False,
    # scripts=["superset/bin/superset"],
    install_requires=requirements,
    author="Anton Ivanov",
    email="a.i.ivanov.sv@gmail.com"
)
