import uuid
import xml.etree.ElementTree as ET
import json
import requests
import urllib
import csv
import uuid
import os
import pandas as pd
import openpyxl
import glob

# filename = "A006371"
# ja = "藜光堂本"

filename = "A006267"
ja = "钟伯敬本"

dir_path = "data/" + filename

files = glob.glob(dir_path + "/*.txt")

map = {}

for i in range(len(files)):
    arr = []
    map[i] = arr
    e = ""

    file_path = dir_path + "/" + ja + str(i) + ".txt"

    f = open(file_path)
    lines2 = f.readlines()
    f.close()
    for line in lines2:
        if line.strip() == "":
            arr.append(e)
            e = ""
        else:
            e = e + line

df = []

for i in map:
    arr = map[i]
    for j in range(len(arr)):
        df.append([i, j, arr[j].split("\n")[0]])

df = pd.DataFrame(df, columns=['a', 'b', 'c'])
df.to_excel('data/' + filename + '.xlsx', index=False)
