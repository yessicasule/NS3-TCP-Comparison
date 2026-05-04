#!/usr/bin/env python3
"""
Windows Setup Script for NS-3 TCP Comparison Project
Installs all required Python dependencies
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python 3.8+ is installed"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher required!")
        return False
    
    print("✓ Python version OK")
    return True

def install_packages():
    """Install required Python packages"""
    packages = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'seaborn'
    ]
    
    print("\n📦 Installing Python packages...")
    
    for package in packages:
        print(f"  Installing {package}...", end=" ")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', package])
            print("✓")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def verify_imports():
    """Verify all packages can be imported"""
    print("\n✓ Verifying imports...")
    
    modules = ['matplotlib', 'numpy', 'pandas', 'scipy', 'seaborn']
    
    for module in modules:
        try:
            __import__(module)
            print(f"  {module}: OK")
        except ImportError:
            print(f"  {module}: FAILED")
            return False
    
    return True

def main():
    print("="*60)
    print("NS-3 TCP Comparison - Windows Setup")
    print("="*60)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install packages
    if not install_packages():
        sys.exit(1)
    
    # Step 3: Verify imports
    if not verify_imports():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\nYou can now run:")
    print("  python plot_graphs.py")
    print("\nPress Enter to continue...")
    input()

if __name__ == '__main__':
    main()
