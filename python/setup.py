import setuptools
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setuptools.setup(
    name="sdc-apis",
    version="0.2.1.dev20240222",
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
    include_package_data=True,
)
