from __future__ import unicode_literals

import re, uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

VERSIONFILE = "zohocrm/__init__.py"
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
with open(VERSIONFILE, "rt") as version_file:
    match = re.search(version_re, version_file.read(), re.M)

if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]

setup(name="zohocrm",
      version=version,
      description="Zoho CRM API library for python",
      license="MIT",
      author="Blitzen",
      author_email="eng@blitzen.com",
      url="https://github.com/Blitzen/zohocrm",
      packages=find_packages(exclude=['tests']),
      install_requires=reqs,
      keywords="zoho crm library",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      zip_safe=True)
