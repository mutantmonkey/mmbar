from setuptools import setup

setup(
    name="mmbar",
    packages=["mmbar"],
    scripts=["mmbar-status"],
    version="2.0",
    description="Python i3bar status line generator",
    license="ISC",
    author="mutantmonkey",
    author_email="mmbar@mutantmonkey.in",
    url="https://github.com/mutantmonkey/mmbar",
    install_requires=["requests>=2.4"]
)
