#!/usr/bin/env python3
"""
Download and install LibreOffice automatically
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import tempfile
from pathlib import Path

def get_libreoffice_download_url():
    """Get the latest LibreOffice download URL for Windows"""
    # LibreOffice download URLs for Windows (updated)
    urls = {
        "64-bit": "https://download.documentfoundation.org/libreoffice/stable/7.6.5/win/x86_64/LibreOffice_7.6.5_Win_x64.msi",
        "32-bit": "https://download.documentfoundation.org/libreoffice/stable/7.6.5/win/x86/LibreOffice_7.6.5_Win_x86.msi"
    }
    
    # Check if system is 64-bit
    if sys.maxsize > 2**32:
        return urls["64-bit"], "LibreOffice_7.6.5_Win_x64.msi"
    else:
        return urls["32-bit"], "LibreOffice_7.6.5_Win_x86.msi"

def download_libreoffice():
    """Download LibreOffice installer"""
    print("📥 Downloading LibreOffice...")
    
    try:
        url, filename = get_libreoffice_download_url()
        print(f"  URL: {url}")
        print(f"  File: {filename}")
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        installer_path = os.path.join(temp_dir, filename)
        
        # Download file
        print("  Downloading (this may take a few minutes)...")
        urllib.request.urlretrieve(url, installer_path)
        
        print(f"  ✓ Download completed: {installer_path}")
        return installer_path
        
    except Exception as e:
        print(f"  ✗ Download failed: {e}")
        return None

def install_libreoffice(installer_path):
    """Install LibreOffice using the downloaded installer"""
    print("🔧 Installing LibreOffice...")
    
    try:
        # Run the installer silently
        cmd = [
            "msiexec",
            "/i", installer_path,
            "/quiet",  # Silent installation
            "/norestart",  # Don't restart
            "/log", "libreoffice_install.log"  # Log file
        ]
        
        print("  Running installer (this may take several minutes)...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("  ✓ LibreOffice installed successfully!")
            return True
        else:
            print(f"  ✗ Installation failed with return code: {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ⏰ Installation timed out (this is normal for large installers)")
        print("  Please check if LibreOffice was installed manually")
        return True
    except Exception as e:
        print(f"  ✗ Installation failed: {e}")
        return False

def check_libreoffice_installation():
    """Check if LibreOffice was installed successfully"""
    print("🔍 Checking LibreOffice installation...")
    
    libreoffice_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        r"C:\Program Files\LibreOffice*\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice*\program\soffice.exe",
    ]
    
    for path in libreoffice_paths:
        try:
            if '*' in path:
                import glob
                matching_paths = glob.glob(path)
                if matching_paths:
                    path = matching_paths[0]
            
            if os.path.exists(path):
                print(f"  ✓ LibreOffice found at: {path}")
                return True
        except:
            continue
    
    print("  ✗ LibreOffice not found")
    return False

def main():
    """Main installation process"""
    print("🚀 LibreOffice Auto-Installer")
    print("=" * 50)
    
    # Check if already installed
    if check_libreoffice_installation():
        print("\n✅ LibreOffice is already installed!")
        return
    
    # Download LibreOffice
    installer_path = download_libreoffice()
    if not installer_path:
        print("\n❌ Failed to download LibreOffice")
        print("Please download manually from: https://www.libreoffice.org/")
        return
    
    # Install LibreOffice
    if install_libreoffice(installer_path):
        print("\n✅ LibreOffice installation completed!")
        
        # Clean up installer
        try:
            os.remove(installer_path)
            os.rmdir(os.path.dirname(installer_path))
        except:
            pass
        
        # Final check
        if check_libreoffice_installation():
            print("🎉 LibreOffice is ready to use!")
            print("\n💡 You can now run the File Monitor with improved DOC conversion:")
            print("   python file_monitor.py")
        else:
            print("⚠️  Installation may have completed, but LibreOffice not detected")
            print("Please restart your computer and try again")
    else:
        print("\n❌ Installation failed")
        print("Please install LibreOffice manually from: https://www.libreoffice.org/")

if __name__ == "__main__":
    main() 