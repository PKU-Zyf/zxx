CALL "D:\anaconda3\Scripts\activate.bat"
E:
cd E:\zyf\publicity\MyProjects\zxx
python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine
python -m twine upload dist/*
% API token 设置参见 C:\Users\PKU-Z\.pypirc %
pause
