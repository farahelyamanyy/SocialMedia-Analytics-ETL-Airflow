# Social Media Analytics Pipeline  

This project demonstrates the development of a **data pipeline** for extracting and processing data from social media APIs. The pipeline collects data (e.g., tweets, video metadata), processes it with Python, and stores it in a structured format for further analysis.  

---

## 📌 Project Overview  

The project highlights key data engineering skills, including:  
- API integration and authentication  
- Data extraction, cleaning, and transformation using **Python and Pandas**  
- Environment variable management for secure credential handling  
- Workflow automation and orchestration (using **Apache Airflow**)  
- Performing various analyses on the loaded data  

---

## 🖥️ Prerequisites  

Before running the pipeline, ensure you have the following installed on your machine:  

- **Docker Desktop**: Recommended way to run Airflow on any operating system (including Windows) as it provides a consistent, isolated Linux environment.  
- **Access to Twitter’s v2 API and YouTube’s Data API v3**:  
  - Obtain a **Bearer Token** for Twitter.  
  - Obtain an **API Key** for YouTube.  

---

## ⚙️ Project Setup  

### 📂 Step 3.1: Project Structure  

```
your_project/
├── dags/                           Contains Airflow DAG Python script.
│ └── social_media_etl.py           
├── .env                            Stores API credentials.
├── requirements.txt                Lists all necessary Python libraries.
└── docker-compose.yaml             Defines Docker services for Airflow.
```

---

### 📝 Step 3.2: Configure Files  

#### `social_media_etl.py`  
Place the entire Python script for the Airflow DAG inside the `dags/` folder.  

#### `.env`  
Create this file in the project’s root directory and add  your API credentials:  

#### `requirements.txt`
Create this file in the project’s root directory and add the required Python packages:

```
pandas
tweepy
python-dotenv
google-api-python-client
apache-airflow
```

#### `docker-compose.yaml`
Create this file in the project’s root directory and copy the content below.
This configuration uses a SQLite backend for simplicity in a local development environment.

```
version: '3.8'
services:
  airflow-webserver:
    image: apache/airflow:2.4.0
    container_name: airflow_webserver
    volumes:
      - ./dags:/opt/airflow/dags
      - ./requirements.txt:/requirements.txt
      - ./.env:/opt/airflow/.env
    env_file:
      - ./.env
    environment:
      - AIRFLOW_PIP_INSTALL_REQUIREMENTS=1
    ports:
      - "8080:8080"
    command: webserver
    restart: always

  airflow-scheduler:
    image: apache/airflow:2.4.0
    container_name: airflow_scheduler
    volumes:
      - ./dags:/opt/airflow/dags
      - ./requirements.txt:/requirements.txt
      - ./.env:/opt/airflow/.env
    env_file:
      - ./.env
    environment:
      - AIRFLOW_PIP_INSTALL_REQUIREMENTS=1
    command: scheduler
    restart: always
```
---
## ▶️ Running the Pipeline  

Follow these steps to start and run your Airflow pipeline using **Docker Compose**:  

1.  **Open your terminal** and navigate to the root of your project directory.
2.  **Start the Airflow services** with Docker Compose:

    ```bash
    docker-compose up -d
    ```

    This command will download the necessary images and start the containers. The dependencies from `requirements.txt` will be automatically installed.

3.  **Access the Airflow UI** at `http://localhost:8080`.
4.  **Log in** with the default credentials: `airflow` / `airflow`.
5.  **Enable the DAG**: In the UI, locate **SocialMedia_ETL** and toggle it **on**.
6.  **Trigger a run**: Click the "play" button to execute the pipeline manually.


---

## 📄 Pipeline Output

Upon completion, the pipeline will generate two CSV files in your project's root directory:

-   `SocialMedia_Analysis.csv`: The combined and transformed raw data.
-   `Analytics_Report.csv`: The final analytical report containing key insights.

