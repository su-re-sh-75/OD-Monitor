import os
import sys
from copy import deepcopy
import re
# print(sys.getsizeof(1))
# var = True
# print(sys.getsizeof(var))
# print(1 << 224)

def filter_cond(string: str) -> bool:
    words_set = frozenset(['od', 'pc', 'list', 'round', 'students', 'student', 'hall', 'shortlisted', 'shortlists', 'shortlist', 'ppt', 'test', 'interview', 'hr'])
    return string.lower() not in words_set and not string.isdigit()

def extract_cmp_name(string: str) -> str:
    words = string.split(" ")
    temp = []
    for word in words:
        arr = word.split("_")
        temp.extend(arr)
    words = deepcopy(temp)
    filtered_words = list(filter(filter_cond, words))
    return " ".join(filtered_words)

paths = []
for filename in os.listdir('All ODs'):
    rem = re.match(r'(\d{4}_\d{2}_\d{2})_([A-Za-z0-9_ &-]+)', filename)
    paths.append(rem.group(2))

# print(paths)
for path in paths:
    print(f'{path} \t {extract_cmp_name(path)}')