### 1. Excel file read and write
```
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data

install module method:
pip install pyexcel-xlsx
```
### 2. Search file in a directory
```
for filename in os.listdir(path):		# Directory path
    if filename.find("%s"%chip_id) != -1:    	# find Chip_ID == filename
```
### 3. Sort file by modified time
  - [Sort file by modified time](https://blog.csdn.net/qq_18525247/article/details/79820246)
