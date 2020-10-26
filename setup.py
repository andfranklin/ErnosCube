from setuptools import setup, find_packages
import sys

project_name = "ErnosCube"
major = 0
minor = 1
verison_number = f"{major}.{minor}"
full_project_name = f"{project_name} {verison_number}"

error_str = "\n\n"
error_str += f"You are running {full_project_name} on Python 2\n\n"
error_str += f"Unfortunately {full_project_name} is not compatible with"
error_str += f"Python 2. Sorry about\nthat. If you want to use {project_name}"
error_str += f" install Python 3.8 or greater, make sure you have\npip >= 20.2"
error_str += f" and setuptools >= 50.3:\n\n"
error_str += f"  $ pip install pip setuptools --upgrade"

if sys.version_info < (3,):
    raise ImportError(error_str)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = [line.rstrip() for line in requirements_file]
    print(requirements)

with open('requirements_test.txt') as test_requirements_file:
    test_requirements = [line.rstrip() for line in test_requirements_file]

setup(
    name=project_name,
    version="0.1.0",
    description="Another Rubik's Cube simulator because ¯\\_(ツ)_/¯",
    long_description=f"{readme}\n\n{history}",
    author="Andrew Franklin",
    author_email="andfranklin3@gmail.com",
    url=f"https://github.com/andfranklin/{project_name}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords="rubiks",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=test_requirements,
    python_requires='>=3.8'
)