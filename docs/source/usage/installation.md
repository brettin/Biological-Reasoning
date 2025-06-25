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
<!-- 
#### Installing from Source with Extra Support Modules

Clone the repository and install the package with desired extras. For instance, to install both MCP and OpenAPI supports:

```bash
git clone https://github.com/brettin/biological-reasoning.git
cd ToolRegistry
pip install .[mcp,openapi,langchain] -->
