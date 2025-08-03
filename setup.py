from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="speedai",
    version="1.0.0",
    author="SpeedAI",
    author_email="team@speedai.chat",
    description="Python package for SpeedAI document and text processing API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SpeedAI-team/speedai-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    keywords="speedai api sdk text-processing document-processing ai",
    project_urls={
        "Documentation": "https://github.com/SpeedAI-team/speedai-py/wiki",
        "Bug Reports": "https://github.com/SpeedAI-team/speedai-py/issues",
        "Source": "https://github.com/SpeedAI-team/speedai-py",
    },
)