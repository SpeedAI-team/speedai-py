# Publishing SpeedAI to PyPI

This guide explains how to publish the SpeedAI Python package to PyPI.

## Prerequisites

1. PyPI account: https://pypi.org/account/register/
2. Test PyPI account (optional): https://test.pypi.org/account/register/
3. API tokens for both PyPI and Test PyPI

## Setup API Tokens

### 1. Create PyPI API Token

1. Log in to [PyPI](https://pypi.org/)
2. Go to Account Settings → API tokens
3. Create a new API token with scope "Entire account" or specific to "speedai"
4. Save the token securely

### 2. Create Test PyPI API Token (Optional)

1. Log in to [Test PyPI](https://test.pypi.org/)
2. Follow the same steps as above

### 3. Add Tokens to GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add two new repository secrets:
   - `PYPI_API_TOKEN`: Your PyPI token
   - `TEST_PYPI_API_TOKEN`: Your Test PyPI token (optional)

## Manual Publishing

### Local Setup

```bash
cd python-sdk
pip install build twine
```

### Build the Package

```bash
python -m build
```

This creates:
- `dist/speedai-1.0.0-py3-none-any.whl` (wheel distribution)
- `dist/speedai-1.0.0.tar.gz` (source distribution)

### Test the Package

```bash
# Check package
twine check dist/*

# Test install locally
pip install dist/speedai-1.0.0-py3-none-any.whl

# Test upload to Test PyPI
twine upload --repository testpypi dist/*
```

### Publish to PyPI

```bash
twine upload dist/*
```

## Automated Publishing with GitHub Actions

The repository includes a GitHub Actions workflow that automatically publishes to PyPI when you create a version tag.

### How to Trigger Automatic Publishing

1. Update version in `setup.py` and `pyproject.toml`
2. Commit your changes
3. Create and push a tag:

```bash
git add .
git commit -m "Bump version to 1.0.1"
git tag python-sdk-v1.0.1
git push origin main
git push origin python-sdk-v1.0.1
```

The workflow will:
1. Build the package
2. Upload to Test PyPI (optional)
3. Upload to PyPI

### Manual Workflow Trigger

You can also manually trigger the workflow:
1. Go to Actions tab in GitHub
2. Select "Publish Python SDK to PyPI"
3. Click "Run workflow"

## Version Management

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking API changes
- MINOR: New features, backwards compatible
- PATCH: Bug fixes

### Update Version

Update version in these files:
1. `setup.py` - `version="1.0.0"`
2. `pyproject.toml` - `version = "1.0.0"`
3. `speedai/__init__.py` - `__version__ = "1.0.0"`

## Testing Before Release

### 1. Run Tests

```bash
pip install -e .[dev]
pytest
```

### 2. Check Code Quality

```bash
black speedai
flake8 speedai
```

### 3. Test Installation

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ speedai

# Test the package
python -c "from speedai import SpeedAIClient; print('Import successful')"
```

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Check if API token is correct
   - Ensure token has correct permissions

2. **Package Name Conflict**
   - The name "speedai" must be unique on PyPI
   - Consider alternative names if taken

3. **Build Errors**
   - Ensure all dependencies are listed in setup.py
   - Check that README.md exists and is valid

### Useful Commands

```bash
# View package info
pip show speedai

# Install specific version
pip install speedai==1.0.0

# Upgrade package
pip install --upgrade speedai

# Uninstall
pip uninstall speedai
```

## Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG
- [ ] Run tests
- [ ] Check code quality
- [ ] Test local installation
- [ ] Create git tag
- [ ] Push to GitHub
- [ ] Verify GitHub Actions success
- [ ] Test PyPI installation
- [ ] Update documentation

## Links

- PyPI: https://pypi.org/project/speedai/
- Test PyPI: https://test.pypi.org/project/speedai/
- GitHub Actions: https://github.com/yourusername/HumanizerAI/actions
- Documentation: https://packaging.python.org/