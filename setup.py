import setuptools

setuptools.setup(
    name="SymPathY",
    version="0.0.1",
    description="SymPathY - A Python package to yield symbolic path descriptions from SVGs.",
    license="MIT",
    author="Armin Steinhauser",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="svg symbolic path arc parametrization frenet automatic differentiation",
    url="https://github.com/asteinh/SymPathY",
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
