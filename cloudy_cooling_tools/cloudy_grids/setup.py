from setuptools import setup

def get_version(filename):
    """
    Get version from a file.

    Inspired by https://github.mabuchilab/QNET/.
    """
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split("=")[1].strip()[1:-1]
    raise RuntimeError(
        "Could not get version from %s." % filename)


VERSION = get_version("cloudy_grids/__init__.py")

# with open('README.md') as f:
#     long_description = f.read()
long_description = ""

setup(name="cloudy_grids",
      version=VERSION,
      description="Tools for converting grids of Cloudy ascii data to hdf5.",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Britton Smith",
      author_email="brittonsmith@gmail.com",
      license="BSD 3-Clause",
      keywords=["astronomy", "astrophysics"],
      url="https://github.com/brittonsmith/cloudy_cooling_tools",
      project_urls={
      },
      packages=["cloudy_grids"],
      include_package_data=True,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Astronomy",
          "License :: OSI Approved :: BSD License",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: Linux",
          "Operating System :: Unix",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      install_requires=[
          'h5py',
          'numpy',
      ],
      python_requires='>=3.6'
)
