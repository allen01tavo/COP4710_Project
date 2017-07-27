# -*- mode: python -*-

block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=['/Users/gmaturan/Documents/SPC/Spring_2015/Python_Projects/Patient'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mainwindow',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mainwindow')
app = BUNDLE(coll,
             name='mainwindow.app',
             icon=None,
             bundle_identifier=None)
