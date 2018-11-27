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

filename = "A006371"
ja = "藜光堂本"
title = "新刻全像忠義水滸誌伝二十五巻一百十五回"

# filename = "A006267"
# ja = "钟伯敬本"
# title = "鍾伯敬先生批評水滸伝一百巻一百回"

dir_path = "data/"+filename

files = glob.glob(dir_path + "/*.txt")

df = pd.read_excel('data/'+filename+'_edited.xlsx')

tmp_path = "data/template.xml"

prefix = ".//{http://www.tei-c.org/ns/1.0}"
xml = ".//{http://www.w3.org/XML/1998/namespace}"

tree = ET.parse(tmp_path)
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

body = root.find(prefix + "body")

p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
body.append(p)

r_count = len(df.index)
c_count = len(df.columns)

manifest_arr = []

excel_map = {}

for i in range(0, r_count):
    file_id = df.iloc[i, 0]
    arr_index = df.iloc[i, 1]

    canvas_id = df.iloc[i, 6]
    manifest = df.iloc[i, 5]

    if file_id not in excel_map:
        excel_map[file_id] = {}

    tmp = excel_map[file_id]

    if not pd.isnull(canvas_id):
        tmp[arr_index] = canvas_id
        if manifest not in manifest_arr:
            manifest_arr.append(manifest)

canvas_image_map = {}

for i in range(len(manifest_arr)):
    url = manifest_arr[i]
    response = urllib.request.urlopen(url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    canvases = data["sequences"][0]["canvases"]

    for j in range(len(canvases)):
        image_url = canvases[j]["images"][0]["resource"]["service"]["@id"];
        image_url = image_url + "/full/400,/0/default.jpg"
        canvas_id = canvases[j]["@id"]
        canvas_image_map[canvas_id] = image_url

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

        pb = ET.Element("{http://www.tei-c.org/ns/1.0}pb")
        p.append(pb)
        pb.set("n", str(j + 1))

        if i in excel_map and j in excel_map[i]:
            canvas_id = excel_map[i][j]
            image_url = canvas_image_map[canvas_id]
            pb.set("facs", image_url)

        arr2 = arr[j].split("\n")
        for k in range(len(arr2)):

            line = arr2[k].strip()
            if line != "":
                lb = ET.Element("{http://www.tei-c.org/ns/1.0}lb")
                p.append(lb)

                span = ET.Element("{http://www.tei-c.org/ns/1.0}span")
                p.append(span)
                span.text = arr2[k]

title_node = root.find(prefix + "title")
title_node.text = title

sourceDesc = root.find(prefix + "sourceDesc")
p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
sourceDesc.append(p)

tree.write("data/"+filename+".xml", encoding="utf-8")
