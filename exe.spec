# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def get_pycache_files(directory):
    pycache_files = []
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in root:
            for file in files:
                if file.endswith('.pyc'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, directory)
                    pycache_files.append((full_path, os.path.dirname(rel_path)))
    return pycache_files

# Dynamically collect all Python modules
def collect_submodules(directory):
    hidden_imports = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                # Convert file path to module path
                module_path = os.path.join(root, file)
                rel_path = os.path.relpath(module_path, directory)
                module_name = rel_path.replace(os.path.sep, '.')[:-3]  # Remove .py
                hidden_imports.append(module_name)
    return hidden_imports

a = Analysis(
    ['main.py'],  # Main script
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('resources', 'resources')
    ],
    hiddenimports=collect_submodules('.') + ['aiomysql'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['*.py'],  
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Subsystem-Service-MySQL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='',
    uac_admin=False  # This enables running as administrator
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Subsystem-Service-MySQL'
)