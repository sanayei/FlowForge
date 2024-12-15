from setuptools import setup, find_packages

setup(
    name="distributed-ocr-pipeline",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.26.0",
        "sagemaker>=2.132.0",
        "pandas>=1.5.0",
        "pytesseract>=0.3.10",
        "pdf2image>=1.16.3",
        "pyarrow>=12.0.1",
        "s3fs>=2023.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.4.1",
            "pylint>=2.17.5",
        ]
    },
    python_requires=">=3.9",
)
