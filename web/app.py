from flask import Flask, render_template, request
from pymongo import MongoClient
import time 

app = Flask(__name__)

client = MongoClient("mongodb+srv://testing_seg:nhatrinh269@cluster0.ui4yvfj.mongodb.net/")
db = client['disease_db_update']

disease_collection = db['disease']
link_collection = db['test1']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    disease = request.form.get('disease')
    type_disease = "Causes"

    results = link_collection.find({
        "$and": [
            {"attribute.Rare disease": disease},
            {"attribute.type": type_disease}
        ],
    },
    {
        "_id": 0
    })

    time.sleep(2)

    description_result = disease_collection.find({"Rare disease": disease})
    diseases = list(results)
    description = list(description_result)
    
    if not diseases or not description:
        no_data_message = "No data found."
        return render_template('index.html', no_data_message=no_data_message)
    else:
        description = description[-1]["attribute"].get(f"{type_disease}", "No description available")
        return render_template('index.html', results=diseases, query=f"{type_disease} of {disease}", desciption=f"{type_disease} of {disease}: {description}")

if __name__ == '__main__':
    app.run(debug=True)