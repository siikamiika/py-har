import os
import setuptools

setuptools.setup(
    name='py-har',
    version='0.1',
    description='HTTP Archive format parser',
    url='https://github.com/siikamiika/py-har',
    author='siikamiika',
    license='MIT',
    py_modules=['py_har'],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False
)
