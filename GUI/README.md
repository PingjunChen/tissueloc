## Convert ui to py
```
$ pyuic5 -x tissueloc.ui -o tissueloc.py
```
# Build exe
```
$ python -m PyInstaller --onefile --noconsole tissueloc.py
```
