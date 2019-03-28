import os
import json
from data_cleaner import CleanData

path = os.path.dirname(__file__)
data_path = os.path.join(path, 'data', 'cached_data.json')
try:
    with open(data_path) as f:
        c_data = CleanData(json.load(f))
except FileNotFoundError:
    print("Run data_cleaner.py first")
