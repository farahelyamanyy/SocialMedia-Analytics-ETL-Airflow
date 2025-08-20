Social Media Analytics Pipeline

This project demonstrates the development of a data pipeline for extracting and processing data from social media APIs. The pipeline collects data (e.g., tweets, video metadata), processes it with Python, and stores it in a structured format for further analysis.


📌 Project Overview

The project highlights key data engineering skills, including:

API integration and authentication

Data extraction, cleaning, and transformation using Python and Pandas

Environment variable management for secure credential handling

Workflow automation and orchestration (if using Apache Airflow)

Performs various analyses on the loaded data


2. Prerequisites
Before running the pipeline, ensure you have the following installed on your machine:

Docker Desktop: This is the recommended way to run Airflow on any operating system (including Windows) as it provides a consistent, isolated Linux environment.

Access to Twitter's v2 API and YouTube's Data API v3. You must obtain a Bearer Token for Twitter and an API Key for YouTube.

3. Project Setup
Follow these steps to set up the project environment:

Step 3.1: Project Structure
Organize your files with the following structure. Create the folders and files as shown:

your_project/
├── dags/
│   └── social_media_etl.py
├── .env
├── requirements.txt
└── docker-compose.yaml
dags/: This directory will contain your Airflow DAG Python script.

.env: This file will store your API credentials.

requirements.txt: This file lists all the necessary Python libraries.

docker-compose.yaml: This file defines the Docker services for Airflow.

Step 3.2: Configure Files
social_media_etl.py: Place your entire Python script for the Airflow DAG inside the dags folder.

.env: Create this file in the project's root directory and add your API credentials.

Code snippet

YOUTUBE_API_KEY="your_youtube_api_key_here"
TWITTER_BEARER_TOKEN="your_twitter_bearer_token_here"
requirements.txt: Create this file in the project's root directory and add the required Python packages.

Plaintext

pandas
tweepy
python-dotenv
google-api-python-client
apache-airflow
docker-compose.yaml: Create this file in the project's root directory and copy the exact content below. This configuration uses a SQLite backend for simplicity in a local development environment.

YAML

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
4. Running the Pipeline
Follow these steps to start and run your Airflow pipeline using Docker Compose:

Open a terminal and navigate to the root directory of your project (where the docker-compose.yaml file is located).

Start the Airflow services by running the following command:

Bash

docker-compose up -d
This command will download the necessary Docker images, create the containers for the webserver and scheduler, and start them in the background. It will also automatically install the dependencies listed in your requirements.txt file inside the containers.

Access the Airflow UI: Once the services are running, open your web browser and go to http://localhost:8080.

Log in: Use the default credentials:

Username: airflow

Password: airflow

Enable the DAG: In the Airflow UI, find the SocialMedia_ETL DAG in the list and toggle the button to turn it on.

Trigger the DAG: To run the pipeline immediately, click on the SocialMedia_ETL DAG name, and then click the play button in the top right to trigger a new DAG run.

5. Output
Upon successful execution, the pipeline will generate the following two CSV files in the root of your project directory:

SocialMedia_Analysis.csv: Contains the combined and transformed data from Twitter and YouTube.

Analytics_Report.csv: Contains the summary reports, including daily engagement, top 5 overall posts, and top 3 posts per platform.
