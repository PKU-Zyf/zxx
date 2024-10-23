CALL "D:\anaconda3\Scripts\activate.bat"
cd C:\
E:
cd E:\zyf\publicity\MyProjects\zxx
python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine
python -m twine upload dist/*
pause
