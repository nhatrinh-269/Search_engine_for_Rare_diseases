from pyspark.sql import SparkSession 
from pymongo import MongoClient 
from bs4 import BeautifulSoup  
import re
import os 

def list_html(folder):
    """
    This function lists all HTML files in a given folder.
    """
    files = []

    for entry in os.listdir(folder):
        if entry.endswith(".html"):
            files.append(entry)

    return files

# Initialize Spark session
spark = SparkSession.builder \
    .appName("data cleaning") \
    .getOrCreate()

# CSV contains some descriptions of some hard-to-find diseases
file_path = "/craw_data/Describe_rare_diseases.csv"
# Read the CSV file into a Spark DataFrame
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Initialize MongoDB client and define the database and collection
client = MongoClient("mongodb+srv://user:passs@cluster0.*******.mongodb.net/")
db = client['disease_db']

# Database contains descriptions of rare diseases
collection = db['disease'] 
# Database for data crawled from the web
link = db['link']

# Collect all rows from the DataFrame
rows = df.collect()

# Insert each row from the DataFrame into the MongoDB collection
for i in rows:
    document = {
        "Rare disease": i['Rare disease'],
        "attribute": {
            "Disease": i['Description'], 
            "Symptoms": i['Symptoms'],
            "Causes": i['Causes'], 
            "Treatment": i['Treatment'],
            "Diagnosis": i['Diagnosis'], 
            "Prevention": i['Prevention'],
            "Side effects": i['Side effects'], 
            "Complications": i['Complications']
        }
    }
    result = collection.insert_one(document)

# Define the folder containing HTML files
folder = "/craw_data/collected_data"
# Get a list of all HTML files in the folder
html_files = list_html(folder)

# Define regular expression patterns for extracting information from the HTML files
pattern1 = r"viết bởi [^·]+ · \d{4} · |viết bởi [^·]+ · \d{4} —"
pattern2 = r"viết bởi [^·]+ · |viết bởi [^·]+ — "
pattern3 = r"\d{1,2} thg \d{1,2}, \d{4} —"
# ... Add more if you want more data cleaning

# Parse, process each HTML file and push to MongoDB
for path in html_files:
    try:
        with open(os.path.join(folder, path), 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with the specified class
        elements = soup.find_all(class_='N54PNb BToiNc cvP2Ce')

        for i in elements:
            soup_ = i
            title = soup_.find('h3', class_='LC20lb MBeuO DKV0Md').get_text()
            url = soup_.find('a', href=True)['href'].replace("https://", "")
            description = soup_.find('div', class_='VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb').get_text()
            source = soup_.find('span', class_='VuuXrf').get_text()
            attribute = path.replace(".html", "").split("_")

            document = {"title": title, "url": url}

            th1 = re.search(pattern1, description)
            th2 = re.search(pattern2, description)
            th3 = re.search(pattern3, description)

            if th3:
                description = description.replace(th3.group(), "").strip()

                # Format the date
                date_parts = th3.group().split()
                day = date_parts[0].zfill(2)
                month = date_parts[2].zfill(2)
                year = date_parts[4][2:]
                formatted_date = f"{day}-{month}-{year}"

                document["description"] = description
                document["date"] = formatted_date

            elif th1:
                description = description.replace(th1.group(), "").strip()

                # Extract author and year information
                author_part = th1.group(1)
                year_part = th1.group(2) if th1.group(2) else th1.group(3)

                document["description"] = description
                document["author"] = author_part
                document["publication_date"] = year_part
            
            elif th2:
                description = description.replace(th2.group(), "").strip()
                author_part = str(th2.group()).replace("viết bởi", "").strip()

                document["description"] = description
                document["author"] = author_part

            else:
                document["description"] = description

            document["from"] = source
            document["attribute"] = {'Rare disease': attribute[1], "type": attribute[0]}
            result = link.insert_one(document)
    except Exception as e:
        print(f"Exception occurred while processing file {path}: {e}")
