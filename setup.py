import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="rtracker",
    version="1.0.0",
    license="BSD",
    maintainer="Tom Masterson",
    maintainer_email="kd7cyu@gmail.com",
    description="Simple application for checking radio equipment in and out.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
