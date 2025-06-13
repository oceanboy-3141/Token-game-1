# 🐍 Setting Up Conda Environment for Token Quest

## Creating a New Conda Environment

### Method 1: Basic Environment Creation
```bash
# Create a new environment with Python 3.9
conda create -n tokenquest python=3.9

# Activate the environment
conda activate tokenquest

# Install required packages
pip install -r simple_requirements.txt
```

### Method 2: Environment with Specific Packages
```bash
# Create environment with packages in one command
conda create -n tokenquest python=3.9 flask werkzeug

# Activate the environment
conda activate tokenquest

# Install remaining packages
pip install tiktoken
```

### Method 3: From Environment File (Advanced)
```bash
# Create environment.yml file first
conda env create -f environment.yml

# Activate the environment
conda activate tokenquest
```

## Environment Management Commands

### Activate Environment
```bash
conda activate tokenquest
```

### Deactivate Environment
```bash
conda deactivate
```

### List Environments
```bash
conda env list
```

### Remove Environment
```bash
conda env remove -n tokenquest
```

### Export Environment
```bash
# Export to file for sharing
conda env export > environment.yml
```

## Running Token Quest

Once your environment is set up:

```bash
# Activate environment
conda activate tokenquest

# Run the web app
python simple_web_app.py

# Or use the batch file (Windows)
start_token_quest.bat
```

## Troubleshooting

### If packages fail to install:
```bash
# Update conda first
conda update conda

# Try installing with conda instead of pip
conda install flask werkzeug

# For tiktoken, use pip (not available in conda)
pip install tiktoken
```

### If environment activation fails:
```bash
# Initialize conda for your shell
conda init

# Restart your terminal/command prompt
# Then try activating again
conda activate tokenquest
```

## Quick Start Script

Create a file called `setup_conda.bat` (Windows) or `setup_conda.sh` (Mac/Linux):

**Windows (setup_conda.bat):**
```batch
@echo off
echo Creating Token Quest conda environment...
conda create -n tokenquest python=3.9 -y
conda activate tokenquest
pip install flask werkzeug tiktoken
echo Environment setup complete!
echo Run: conda activate tokenquest
pause
```

**Mac/Linux (setup_conda.sh):**
```bash
#!/bin/bash
echo "Creating Token Quest conda environment..."
conda create -n tokenquest python=3.9 -y
conda activate tokenquest
pip install flask werkzeug tiktoken
echo "Environment setup complete!"
echo "Run: conda activate tokenquest"
```

## Environment.yml File

Create this file for easy environment recreation:

```yaml
name: tokenquest
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.9
  - flask
  - werkzeug
  - pip
  - pip:
    - tiktoken
```

Then use: `conda env create -f environment.yml` 