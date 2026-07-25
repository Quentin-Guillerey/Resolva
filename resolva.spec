# resolva.spec  — PyInstaller v6 format
# Build with:  pyinstaller resolva.spec
#
# Produces a single-file executable that starts the Flask server locally and
# opens Resolva in the default browser. No Python install needed on the host.
#
# Must be built on the OS you want to ship to (PyInstaller does not
# cross-compile): build the Windows .exe on Windows.
#
# NOTE: this spec targets PyInstaller v6+. The v5 constructs (block_cipher,
# cipher=, a.zipped_data, a.zipfiles, win_no_prefer_redirects,
# win_private_assemblies) were removed in v6 and cause an immediate build
# failure — same fix already applied to the CSR Automation Toolkit spec.

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    # Bundle the templates, CSS, and demo CSV next to the code so the
    # packaged app can find them via the resource_path() helper in app.py.
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'resolva.config', 'resolva.store', 'resolva.audit',
        'resolva.classifier', 'resolva.ai', 'resolva.ingestion',
        'resolva.accounts', 'resolva.notify',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Resolva',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # no console window; it's a browser app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,            # add icon='resolva.ico' once you have one
)
