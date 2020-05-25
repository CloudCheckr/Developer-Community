import setuptools

install_requires = [
    "requests"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccgetusers",
    version="0.0.1",
    author="Alec Rajeev",
    author_email="alecinthecloud@gmail.com",
    description="Package for getting a list of users from cloudcheckr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudcheckr/Developer-Community/",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.5',
    entry_points={'console_scripts': ['ccgetusers=ccgetusers.command_line:main']},
)
