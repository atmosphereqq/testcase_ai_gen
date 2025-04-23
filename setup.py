from setuptools import setup, find_packages

setup(
    name="swagger_testgen",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=5.4.1',
        'jsonschema>=4.0.0',
        'requests>=2.26.0',
        'pytest>=7.0.0',
        'jinja2>=3.0.0'
    ],
    entry_points={
        'console_scripts': [
            'swagger-testgen=swagger_testgen.main:main'
        ]
    },
    python_requires='>=3.8',
)
