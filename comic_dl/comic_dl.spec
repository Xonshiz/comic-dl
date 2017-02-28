# -*- mode: python -*-

block_cipher = None


a = Analysis(['comic_dl.py'],
             pathex=['C:\\Users\\Psychotic Elites\\Documents\\GitHub\\comic-dl\\comic_dl'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='comic_dl',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\Psychotic Elites\\Documents\\GitHub\\comic-dl\\Images\\Logo.ico')
