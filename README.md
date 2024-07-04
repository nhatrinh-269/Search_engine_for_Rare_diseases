# Search Engine for Rare Diseases
## Overview
Building a rare disease search engine to improve access for patients and researchers. This project aims to provide a centralized platform to search and retrieve relevant information about various rare diseases, thereby facilitating better understanding, research and treatment. In this project, the raw data could be up to 34gb but due to hardware limitations we were only able to collect about 10gb of raw data.

### **Key Features:**
- **Comprehensive data collection**: Synthesize data from multiple sources to ensure comprehensive coverage of rare diseases.

- **User-friendly interface**: Intuitive web interface makes navigation and use easy.
- **Machine learning integration**: Uses machine learning models to improve search accuracy and relevance.
## Project Structure
```
.
├── Search Engine for Rare Diseases
│   ├── craw_data
│   │   ├── collection_data
│   │   │   ├── craw_data.py
│   │   │   ├── push_to_mongo.py
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt
│   │   │   ├── Describe_rare_diseases.csv
│   │   │   └── rare_diseases.csv
│   │   ├── collected_data
│   │   │   ├── Prevention_of_Essential_Thrombocythemia.html
│   │   │   └── Treatment_of_Wolfram_Syndrome.html
│   │   ├── docker-compose.yml
│   ├── web
│   │   ├── templates
│   │   │   └── index.html
│   │   ├── models
│   │   │   ├── label_encoder.pkl
│   │   │   ├── model_weights.pth
│   │   │   └── tokenizer.pkl
│   │   └── app.py
│   └── training_model.py
```


### Explanation

#### `craw_data`
This directory contains scripts and files related to data collection and preprocessing.

- **`collection_data`**: Contains scripts and files for collecting and processing data.
  - **`craw_data.py`**: Script to crawl data from various sources related to rare diseases.
  - **`push_to_mongo.py`**: Script to push the collected data into a MongoDB database for storage and retrieval.
  - **`Dockerfile`**: Contains instructions to build a Docker image for the data collection process.
  - **`requirements.txt`**: Lists Python dependencies needed for the data collection scripts.
  - **`Describe_rare_diseases.csv`**: A CSV file containing descriptions of various rare diseases.
  - **`rare_diseases.csv`**: A CSV file with data on rare diseases.

- **`collected_data`**: Stores the HTML files of the collected data.
  - **`Prevention_of_Essential_Thrombocythemia.html`**: HTML file with information on the prevention of Essential Thrombocythemia.
  - **`Treatment_of_Wolfram_Syndrome.html`**: HTML file with information on the treatment of Wolfram Syndrome.

- **`docker-compose.yml`**: Configuration file for Docker Compose, used to set up and run multi-container Docker applications.

#### `web`
This directory contains the web application files, including templates, models, and the main application script.

- **`templates`**: Directory for HTML templates.
  - **`index.html`**: The main HTML template for the web application interface.

- **`models`**: Directory for storing machine learning models and related files.
  - **`label_encoder.pkl`**: Pickle file of the label encoder used for encoding disease labels.
  - **`model_weights.pth`**: Weights of the trained machine learning model.
  - **`tokenizer.pkl`**: Pickle file of the tokenizer used for processing text data.

- **`app.py`**: The main Python script for the web application. It handles routing, user input, and integration with the machine learning models.

#### `training_model.py`
Script for training the machine learning model used in the search engine. This includes data preprocessing, model training, and evaluation.



## Summary

### **Potential**

### **Limitations**
- **Accuracy of data**: The accuracy of data collected depends on the reliability of the source.
- **Model performance**: The performance of the search function is tied to the performance of the machine learning models used.
- **Scalability issues**: Processing large volumes of data and user queries can require significant computational resources.
## Contribution

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
### **Explanation**
