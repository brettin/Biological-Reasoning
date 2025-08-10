# Installation

[![PyPI version](https://badge.fury.io/py/bio-reasoning.svg)](https://badge.fury.io/py/bio-reasoning)

## Prerequisites

Before setting up Bio-Reasoning, ensure you have the following installed:

- **Python >= 3.10** is required.
- We recommend using `conda/mamba` or `pipx` to manage isolated environments.  
  Download Conda/Mamba from: [Conda Forge](https://conda-forge.org/download/)

## Installation via pip

### Basic Installation

Install the core package (requires **Python >= 3.10**):

```bash
pip install bio-reasoning
```

<!--
### Installing with Extra Support Modules

Extra modules can be installed by specifying extras in brackets. This method accommodates additional modules as the project evolves.

For example, to install specific extra supports:

```bash
pip install toolregistry[mcp,openapi]
```

Below is a table summarizing available extra modules:

| Extra Module | Python Requirement | Example Command                     |
|--------------|--------------------|-------------------------------------|
| mcp          | Python >= 3.10     | pip install toolregistry[mcp]       |
| openapi      | Python >= 3.8      | pip install toolregistry[openapi]   |
| langchain    | Python >= 3.9      | pip install toolregistry[langchain] | -->

### Installation from Source

#### Basic Installation from Source

```bash
git clone https://github.com/brettin/biological-reasoning.git
cd biological-reasoning
pip install .
```

### Development Installation

For developers who want to contribute to the project or work with the latest source code, use the editable installation method:

```bash
# Create a new conda environment
conda create -n bio_reason python==3.10
conda activate bio_reason

# Verify pip location (should be in the conda environment)
which pip

# Install in editable mode
pip install --editable .
```

#### What does `pip install --editable .` do?

The `--editable` flag (or `-e`) installs the package in "editable" or "development" mode. This means:

- **Live Code Changes**: Any changes you make to the source code in the `src/` directory will be immediately available without reinstalling the package
- **Development Workflow**: Perfect for active development where you're frequently modifying code
- **Symlink Installation**: Creates a link to your source code rather than copying files to the site-packages directory
- **Version Control Friendly**: Your changes are tracked in your local git repository and can be easily committed

This is the recommended approach for developers who plan to modify the codebase or contribute to the project.

<!--
#### Installing from Source with Extra Support Modules

Clone the repository and install the package with desired extras. For instance, to install both MCP and OpenAPI supports:

```bash
git clone https://github.com/brettin/biological-reasoning.git
cd ToolRegistry
pip install .[mcp,openapi,langchain] -->
