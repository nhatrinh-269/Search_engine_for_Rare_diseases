from pyspark.sql import SparkSession
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import os

def list_html(folder):
  files = []

  for entry in os.listdir(folder):
    if entry.endswith(".html"):
      files.append(entry)

  return files

spark = SparkSession.builder \
    .appName("data cleaning") \
    .getOrCreate()

file_path = "Describe_rare_diseases.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")
db = client['disease_db']
collection = db['disease']
collection = db['link']

rows = df.collect()

for i in rows:
    document = {
            "Rare disease" : i['Rare disease'],
            "attribute" : {
                "Disease" : i['Description'], 
                "Symptoms" : i['Symptoms'],
                "Causes" : i['Causes'], 
                "Treatment" : i['Treatment'],
                "Diagnosis" : i['Diagnosis'], 
                "Prevention" : i['Prevention'],
                "Side effects" : i['Side effects'], 
                "Complications" : i['Complications']
            }
        }
    result = collection.insert_one(document)

folder = "path/to/html"
html_ = list_html(folder)

pattern1 = r"viết bởi [^·]+ · \d{4} · |viết bởi [^·]+ · \d{4} —"
pattern2 = r"viết bởi [^·]+ · |viết bởi [^·]+ — "
pattern3 = r"\d{1,2} thg \d{1,2}, \d{4} —"

for path in html_:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        elements = soup.find_all(class_='N54PNb BToiNc cvP2Ce')

        for i in elements:
            soup_ = i
            title = soup_.find('h3', class_='LC20lb MBeuO DKV0Md').get_text()
            url = soup_.find('a', href=True)['href'].replace("https://","")
            description = soup_.find('div', class_='VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb').get_text()
            source = soup_.find('span', class_='VuuXrf').get_text()
            attribute = path.replace(".html","").split("_")

            document = {"title":title,"url":url}

            th1 = re.search(pattern1,description)
            th2 = re.search(pattern2,description)
            th3 = re.search(pattern3,description)

            if th3:
                description = description.replace(th3.group(),"").strip()

                day = th3.group(1)
                month = th3.group(2)
                year = th3.group(3)[2:]
                formatted_date = f"{day.zfill(2)}-{month.zfill(2)}-{year}"

                document["description"] = description
                document["date"] = formatted_date

            elif th1:
                description = description.replace(th1.group(),"").strip()

                author_part = th1.group(1)
                year_part = th1.group(2) if th1.group(2) else th1.group(3)

                document["description"] = description
                document["author"] = author_part
                document["publication_date"] = year_part
            
            elif th2:
                description = description.replace(th2.group(),"").strip()
                author_part = str(th2.group()).replace("viết bởi").strip()

                document["description"] = description
                document["author"] = author_part

            else:
                document["description"] = description

            document["from"] = source
            document["attribute"] = {'Rare disease' : attribute[1],"type" : attribute[0]}
            result = collection.insert_one(document)
    except:
        pass