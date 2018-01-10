pyinstaller --onefile --hidden-import=queue --icon="Logo.ico" "__main__.py"
cd dist
upx.exe "__main__.exe" --best