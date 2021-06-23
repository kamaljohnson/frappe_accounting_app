from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in frappe_accounting_app/__init__.py
from frappe_accounting_app import __version__ as version

setup(
	name='frappe_accounting_app',
	version=version,
	description='An app to manage all the accounting needs of a company',
	author='Kamal Johnson',
	author_email='kamal@erpnext.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
