### 1. Excel file read and write
```python
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data

install module method:
pip install pyexcel-xlsx
```
### 2. Search file in a directory
```python
for filename in os.listdir(path):		# Directory path
    if filename.find("%s"%chip_id) != -1:    	# find Chip_ID == filename
```
### 3. Sort file by modified time
  - [Sort file by modified time](https://blog.csdn.net/qq_18525247/article/details/79820246)
### 4. File related link
  - [File related link](https://blog.csdn.net/w122079514/article/details/16864403)
