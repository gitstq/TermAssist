#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for TermAssist
打包脚本
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True


def clean_build():
    """Clean build artifacts"""
    dirs_to_remove = ['build', 'dist', '*.egg-info', '__pycache__', '.pytest_cache']
    for pattern in dirs_to_remove:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                print(f"Removing {path}")
                shutil.rmtree(path)
    
    # Remove .pyc files
    for pyc in Path('.').rglob('*.pyc'):
        pyc.unlink()
    for pycache in Path('.').rglob('__pycache__'):
        if pycache.is_dir():
            shutil.rmtree(pycache)


def install_dependencies():
    """Install dependencies"""
    return run_command("pip install -r requirements.txt")


def run_tests():
    """Run tests"""
    return run_command("python -m pytest tests/ -v")


def build_package():
    """Build Python package"""
    return run_command("python -m build")


def build_executable():
    """Build standalone executable with PyInstaller"""
    system = platform.system().lower()
    
    # Install pyinstaller if not present
    run_command("pip install pyinstaller")
    
    cmd = (
        f"pyinstaller --onefile "
        f"--name termassist-{system} "
        f"--hidden-import=rich "
        f"--hidden-import=pyyaml "
        f"--hidden-import=requests "
        f"--hidden-import=ollama "
        f"--hidden-import=openai "
        f"--hidden-import=anthropic "
        f"--hidden-import=click "
        f"--hidden-import=prompt_toolkit "
        f"--hidden-import=pyperclip "
        f"termassist/main.py"
    )
    
    return run_command(cmd)


def main():
    """Main build process"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build TermAssist")
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--package', action='store_true', help='Build Python package')
    parser.add_argument('--exe', action='store_true', help='Build executable')
    parser.add_argument('--all', action='store_true', help='Run full build process')
    
    args = parser.parse_args()
    
    if args.clean or args.all:
        clean_build()
    
    if args.all:
        if not install_dependencies():
            print("Failed to install dependencies")
            sys.exit(1)
        
        if not run_tests():
            print("Tests failed")
            sys.exit(1)
        
        if not build_package():
            print("Package build failed")
            sys.exit(1)
        
        if not build_executable():
            print("Executable build failed")
            sys.exit(1)
        
        print("\n✅ Build completed successfully!")
        print("📦 Package: dist/")
        print("🚀 Executable: dist/termassist-*")
    
    elif args.test:
        if not run_tests():
            sys.exit(1)
    
    elif args.package:
        if not build_package():
            sys.exit(1)
    
    elif args.exe:
        if not build_executable():
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
