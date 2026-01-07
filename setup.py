# ============================================================================
# FILE: setup.py
# ============================================================================
"""
Setup script for package installation.
"""
from setuptools import setup, find_packages

setup(
    name='logistics-ml-platform',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Production-ready ML platform for logistics risk prediction',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'scikit-learn>=1.3.0',
        'xgboost>=2.0.0',
        'Flask>=3.0.0',
        'joblib>=1.3.0',
        'python-dateutil>=2.8.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

