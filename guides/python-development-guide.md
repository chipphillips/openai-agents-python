# Python Development Guide

## Environment Details

### Installation

- Python Version: 3.12.8
- Architecture: ARM64
- Installation Path: `C:\Users\chipp\AppData\Local\Programs\Python\Python312-arm64`
- Python Launcher: `py.exe` (Version 3.12.81503)

### System Configuration

- OS: Windows 11 (ARM64)
- PowerShell Core: 7.4.6
- Environment Variables:
  - Python Path: Added to User PATH
  - Scripts Path: Added to User PATH

## Usage

### Command Line Access

Python can be accessed in two ways:

1. Using `python` command directly:

   ```powershell
   python --version
   ```

2. Using Python Launcher (recommended for multiple Python versions):

   ```powershell
   py --version
   ```

### PowerShell Integration

Following our coding standards, use PowerShell syntax for Python operations:

```powershell
# Run Python script
& python script.py

# Run Python module
& python -m module_name

# Install packages
& python -m pip install package_name
```

### Virtual Environments

For project isolation, create virtual environments:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate
```

### Package Management

Use pip for package management:

```powershell
# Update pip
python -m pip install --upgrade pip

# Install packages
python -m pip install package_name

# Install from requirements.txt
python -m pip install -r requirements.txt

# Generate requirements.txt
python -m pip freeze > requirements.txt
```

## Best Practices

### Project Structure

```file structure
project/
├── app/                # Next.js App Router directory
│   ├── api/           # API routes
│   ├── (features)/    # Feature routes
│   └── layout.tsx     # Root layout
├── components/        # React components
├── lib/              # Python utilities and helpers
├── config/           # Configuration files
├── tests/            # Test files
├── public/           # Static assets
├── .venv/            # Virtual environment (git-ignored)
├── requirements.txt  # Python dependencies
└── README.md        # Documentation
```

### Environment Management

1. Always use virtual environments for projects
2. Keep `requirements.txt` updated
3. Use `.gitignore` for Python-specific files:

   ```gitignore
   .venv/
   __pycache__/
   *.pyc
   .pytest_cache/
   ```

### ARM64 Considerations

1. Use native ARM64 packages when available
2. Some packages may run under emulation
3. Check package compatibility before installation

## Troubleshooting

### Common Issues

1. Python not found:

   ```powershell
   # Verify Python in PATH
   Get-Command python
   ```

2. Package installation fails:

   ```powershell
   # Use --verbose for more information
   python -m pip install package_name --verbose
   ```

3. Virtual environment issues:

   ```powershell
   # Recreate virtual environment
   Remove-Item -Recurse -Force .venv
   python -m venv .venv
   ```

### Support Resources

- [Python Documentation](https://docs.python.org/3.12/)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [venv Documentation](https://docs.python.org/3/library/venv.html)

## Getting Started with Python

### Creating Python Scripts

Python files use the `.py` extension. Create them using any text editor or IDE:

```powershell
# Create a new Python file
New-Item -ItemType File -Path "hello.py"
```

Basic script structure:

```python
#!/usr/bin/env python3
"""
Description of what your script does
"""

# Import statements at the top
import os
import sys

# Constants (use UPPERCASE)
MAX_RETRIES = 3
DEFAULT_PATH = "data"

# Function definitions
def main():
    """Main function that runs when script is executed"""
    print("Hello, World!")

# Standard boilerplate for running scripts
if __name__ == "__main__":
    main()
```

### Running Python Scripts

1. Direct execution:

   ```powershell
   # Run script
   python script.py

   # Run with arguments
   python script.py arg1 arg2
   ```

2. Make script executable (optional):

   ```python
   # Add to top of script
   #!/usr/bin/env python3
   ```

### Example Tool: File Organizer

Here's a complete example of a simple tool that organizes files by extension:

```python
#!/usr/bin/env python3
"""
File Organizer Tool
Organizes files in a directory by their extension.
"""

import os
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants
DEFAULT_PATH = "."
IGNORE_DIRS = {".git", "__pycache__", ".venv"}

def setup_directory(base_path: str) -> None:
    """Create organization directories if they don't exist."""
    categories = ["Documents", "Images", "Code", "Others"]
    for category in categories:
        Path(base_path).joinpath(category).mkdir(exist_ok=True)

def get_category(file_ext: str) -> str:
    """Determine category based on file extension."""
    ext_mapping = {
        # Documents
        "doc": "Documents", "docx": "Documents", "pdf": "Documents", "txt": "Documents",
        # Images
        "jpg": "Images", "jpeg": "Images", "png": "Images", "gif": "Images",
        # Code
        "py": "Code", "js": "Code", "html": "Code", "css": "Code",
        # Default
        "": "Others"
    }
    return ext_mapping.get(file_ext.lower().lstrip("."), "Others")

def organize_files(directory: str = DEFAULT_PATH) -> None:
    """Organize files in the specified directory."""
    try:
        # Convert to absolute path
        directory = str(Path(directory).resolve())
        
        # Setup organization directories
        setup_directory(directory)
        
        # Scan and organize files
        for item in Path(directory).iterdir():
            # Skip if it's a directory or ignored
            if item.is_dir() or item.name in IGNORE_DIRS:
                continue
                
            # Get category and create destination path
            category = get_category(item.suffix)
            dest_dir = Path(directory).joinpath(category)
            
            # Move file
            try:
                shutil.move(str(item), str(dest_dir.joinpath(item.name)))
                logging.info(f"Moved {item.name} to {category}")
            except Exception as e:
                logging.error(f"Failed to move {item.name}: {e}")
    
    except Exception as e:
        logging.error(f"Error organizing files: {e}")

def main():
    """Main function."""
    import argparse
    
    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type."
    )
    parser.add_argument(
        "-d", "--directory",
        default=DEFAULT_PATH,
        help="Directory to organize (default: current directory)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run organization
    logging.info(f"Starting file organization in: {args.directory}")
    organize_files(args.directory)
    logging.info("File organization completed")

if __name__ == "__main__":
    main()

### Tool Project Structure
For Python tools, use this structure:
```

file_organizer/                  # Project root
├── .venv/                      # Virtual environment
├── src/                        # Source code
│   └── file_organizer/        # Main package
│       ├── __init__.py        # Makes directory a package
│       ├── main.py            # Main script
│       └── utils.py           # Utility functions
├── tests/                      # Test files
│   ├── __init__.py
│   └── test_organizer.py
├── requirements.txt            # Project dependencies
├── README.md                   # Documentation
└── setup.py                   # Installation configuration

### Running the Example Tool

1. Create project structure:

    ```powershell
   # Create project directory
   New-Item -ItemType Directory -Path "file_organizer"
   Set-Location file_organizer

   # Create virtual environment
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Create project structure
   New-Item -ItemType Directory -Path "src/file_organizer"
   New-Item -ItemType Directory -Path "tests"
     ```

2. Save the script:

   ```powershell
   # Create main script
   New-Item -ItemType File -Path "src/file_organizer/main.py"
   # Copy the example code into main.py
    ```

3. Run the tool:

   ```powershell
   # Run in current directory
   python src/file_organizer/main.py

   # Run in specific directory
   python src/file_organizer/main.py -d "C:\Users\chipp\Downloads"
   ```

### Python Development Tips

1. Use f-strings for string formatting:

   ```python
   name = "World"
   print(f"Hello, {name}!")  # Better than "Hello, " + name + "!"
    ```

2. Handle errors with try/except:

   ```python
   try:
       # Code that might fail
       result = risky_operation()
   except Exception as e:
       # Handle the error
       logging.error(f"Operation failed: {e}")
   ```

3. Use type hints for better code clarity:

   ```python
   def greet(name: str) -> str:
       return f"Hello, {name}!"
   ```

4. Document your code:

   ```python
   def calculate_total(items: list[float]) -> float:
       """
       Calculate the total sum of items.
       
       Args:
           items: List of prices to sum
           
       Returns:
           Total sum of all items
       """
       return sum(items)
   ```
