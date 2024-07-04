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
- **Docker** [here](https://docs.docker.com/get-docker/).
- **Docker-compose** [here]( https://docs.docker.com/compose/).
- **Python** [here](https://www.python.org/downloads/).
- **MongoDB Atlas** [here](https://www.mongodb.com/try/download/atlas-kubernetes-operator).
  
## Required Skills
- **Python**
- **Docker**
- **MongoDB**
- **ETL**
- **NPL**
- **HTML**

## Installation Instructions
1. **Install Docker and Docker Compose:**
   - Download and install Docker from [here]( https://docs.docker.com/compose/install/).
   - Download and install Docker Compose from [here](https://docs.docker.com/compose/install/).
   - Download and install MongoDB Atlas from [here](https://www.mongodb.com/try/download/atlas-kubernetes-operator)
   - Download and install Python from .[here](https://www.python.org/downloads/).
2. **Clone the Repository:**
   ```bash
   git clone https://github.com/nhatrinh-269/Search_engine_for_Rare_diseases
   cd Search_engine_for_Rare_diseases
   ```

### Usage Instructions
- **Build and Run Docker Compose for crawl data:**
   ```bash
   cd craw_data
   docker-compose up --build
   ```
- **Training model:**
  ```bash
  python training_model.py
  ```
- **Run search engine:**
  ```bash
  cd web
  python app.py
  ```
- **Accessing Search Engine:**
   - Visiting `http://127.0.0.1:5000` in a browser loads Search Engine.
     
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
  - **`push_to_mongo.py`**: Script to clean and push the collected data into a MongoDB database for storage and retrieval.
  - **`Dockerfile`**: Contains instructions to build a Docker image for the data collection process.
  - **`requirements.txt`**: Lists Python dependencies needed for the data collection scripts.
  - **`Describe_rare_diseases.csv`**: A CSV file containing descriptions of various rare diseases. We have collected them from [here](https://rarediseases.org/rare-diseases/).
  - **`rare_diseases.csv`**: A CSV file with data on rare diseases. Similar to above, we also collect words [here](https://rarediseases.org/rare-diseases/).

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

### **MongoDB Connection String**

To connect to a MongoDB database, you need to configure your connection string. Follow these steps to set up your MongoDB connection:

1. **Obtain Connection String:**
   - Sign up or log in to your MongoDB account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a new cluster or use an existing one.
   - Navigate to the "Connect" section of your cluster and choose "Connect your application."
   - Copy the connection string provided, which will look something like this:
     ```
     mongodb+srv://user:pass@cluster0.*******.mongodb.net/
     ```

2. **Reference the Connection String in Your Code:**
   - Ensure your scripts reference this connection string when establishing a connection to the database. For example, in your Python script:
     
     ```python
     from pymongo import MongoClient

     client = MongoClient("mongodb+srv://user:pass@cluster0.*******.mongodb.net/")
     db = client.your_database_name
     ```

By following these steps, you'll ensure that your application can connect to and interact with your MongoDB database using the connection string.


## Summary

The Search Engine for Rare Diseases project aims to create a centralized and user-friendly platform for patients and researchers to access information on rare diseases. By leveraging data from diverse sources and utilizing MongoDB for flexible and scalable storage, the search engine will offer efficient and accurate search capabilities. The project employs machine learning to optimize search complexity, ensuring quick retrieval of relevant information. This high-performance search engine will enhance the accessibility and usability of rare disease information, facilitating better patient outcomes and advancing medical research.

### **Potential**

The Search Engine for Rare Diseases has the potential to significantly impact the healthcare and research community by:

- **Enhancing Research**: Providing researchers with a comprehensive and easily accessible database, facilitating deeper insights and advancements in the study and treatment of rare diseases.
- **Improving Patient Care**: Offering patients and healthcare providers quick access to relevant and reliable information, leading to better-informed treatment decisions and improved patient outcomes.
- **Reducing Search Complexity**: Utilizing machine learning to achieve efficient data retrieval, reducing the time and effort required to find pertinent information.
- **Scalability**: Leveraging MongoDB's flexible schema and scalability to handle increasing data volumes as more rare diseases and related research are added to the database.
- **User Accessibility**: Delivering a seamless and intuitive search experience accessible to a wide range of users, from medical professionals to patients and caregivers.
- **Data Integration**: Integrating data from diverse sources, including research papers, specialized medical websites, and reputable articles, to provide a well-rounded and comprehensive repository of information.
- **Supporting Rare Disease Awareness**: Raising awareness about rare diseases by making information more accessible and understandable, thereby contributing to global health initiatives.



### **Limitations**
- **Data Quality, Accuracy, and Integration**: The reliability of the search engine depends on the quality and accuracy of the collected data. Integrating diverse sources can cause inconsistencies and redundancies, requiring significant effort to clean and standardize. Inconsistent or outdated information may affect search results.
- **Hardware and Scalability Constraints**: Hardware limitations only allow partial data collection and processing, limiting the comprehensiveness of the database. Handling large volumes of data and user queries requires significant computational resources.
- **Machine Learning**: The effectiveness of the machine learning model depends on the quality of training data and the chosen algorithms. Poorly trained models may result in inaccurate search results and predictions.
- **Dependence on External Sources**: The project relies on data from external sources, which may change, restrict access, or become unavailable, impacting the search engine's effectiveness.

  
## Contribution
If you want to contribute to this project, please contact me via email `nhatrinh.26902@gmail.com`

## License

This project is licensed under the MIT License - see file [LICENSE](LICENSE) for details.

---

Feel free to further customize according to your project's specific requirements.
