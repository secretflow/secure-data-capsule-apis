import setuptools
from pathlib import Path
from datetime import date

__version__ = "0.3.0.dev$$DATE$$"


def get_version():
    date_str = date.today().strftime("%Y%m%d")
    return __version__.replace("$$DATE$$", date_str)


def read(fname):
    with open(Path(__file__).resolve().parent / Path(fname)) as f:
        return f.read()


setuptools.setup(
    name="sdc-apis",
    version=get_version(),
    author="secretflow",
    author_email="secretflow-contact@service.alipay.com",
    description="SecretFlow Data Capsule apis proto generated python",
    long_description_content_type="text/markdown",
    long_description="SecretFlow Data Capsule apis proto generated python",
    license="Apache 2.0",
    url="https://github.com/secretflow/secure-data-capsule-apis",
    packages=setuptools.find_packages(),
    install_requires=read("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    options={
        "bdist_wheel": {"plat_name": "manylinux2014_x86_64"},
    },
    include_package_data=True,
)
