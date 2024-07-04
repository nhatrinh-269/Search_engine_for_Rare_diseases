# Search Engine for Rare Diseases
## Overview

This project aims to provide a **centralized platform** that allows **patients** and **researchers** to easily search for and retrieve **information related to rare diseases**. The **search engine** will facilitate **better understanding**, **research**, and **treatment** of rare diseases. 

### Data Collection

We collect data from various sources via **Google**, including **research papers**, **specialized medical websites**, and other **reputable sources**. The total amount of **raw data** can reach up to **34GB** or more, depending on the number of **keywords** selected. Due to hardware limitations, we will collect approximately **10GB** of raw data.

### Database Choice

We have chosen **MongoDB** as our primary **database** due to its **flexibility** in handling **non-linear data** and its ease of **scalability**. MongoDB allows us to store and manage a large volume of **unstructured data** efficiently.

### Search Optimization

With **traditional methods**, user input data is **vectorized** and then matched with each **vectorized data field** in the database, resulting in a **search algorithm complexity of O(n)**. We propose using **machine learning** to reduce the algorithm's complexity to **O(1)**. Each data field in the database is **labeled** and **indexed** using **Index1D** in MongoDB. A model is trained to predict which label the user input belongs to, significantly reducing the search algorithm's complexity.

### High-Performance Search Engine

With this approach, we aim to deliver a **high-performance search engine** that reduces **search complexity**, enabling **faster retrieval times** and quick access to **relevant information**. The model's **accurate label predictions** will ensure the retrieval of the most relevant data, enhancing the **quality** and **reliability** of the information. MongoDB's **flexible schema** and **scalability** will handle increasing data as more rare diseases are added. The seamless and intuitive **search experience** will be accessible to a wide range of users, from **medical professionals** to **patients**. Researchers will benefit from the **comprehensive** and **accessible database**, facilitating deeper insights and advancements in the study and treatment of rare diseases.

Overall, this innovative approach will significantly **improve the accessibility** and **usability** of information on rare diseases, contributing to **better patient outcomes** and advancing **medical research**.

### **Key Features:**

- **Data Collection**: Collects data from **diverse sources** including **articles**, **research papers**, and **websites**.

- **MongoDB**: Utilizes MongoDB for its **ease of storage** and **scalability capabilities**.

- **Optimized Search**: Implements **Machine Learning** to achieve **O(1) complexity** for **efficient data retrieval**.

- **User-Friendly Interface**: Provides a **seamless** and **intuitive interface** for enhanced **user interaction**.

- **Enhanced Accessibility**: Facilitates **improved access to information** for both **patients** and **researchers**.

## System Requirements
- **Docker 25.0.5** [here](https://docs.docker.com/get-docker/).
- **Docker-compose 2.27.0** [here]( https://docs.docker.com/compose/).
- **Python 3.9 or higher** [here](https://www.python.org/downloads/).
- **MongoDB 4.4 or higher** [here](https://www.mongodb.com/).
  
## Required Skills
- **Python**
- **Docker**
- **MongoDB**
- **ETL**
- **NPL**
- **HTML**

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
