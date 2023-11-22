Podcast Summary Data Pipeline with Apache Airflow
This repository contains a data engineering project that leverages Apache Airflow to automate the retrieval, storage, and accessibility of podcast episodes. The main components of the project include:

DAG Configuration: The podcast_summary DAG is configured to run daily, starting from November 5, 2023, with tasks for PostgreSQL table creation, podcast information retrieval, and storage optimization.

Tasks:

create_dbtask: Creates a PostgreSQL table to store episode details.
get_episodes: Retrieves podcast information from a specified URL, parses XML responses, and identifies new episodes.
load_apisodes: Compares retrieved episodes with existing database records, updating the database with new episodes.
download_podcasts: Downloads the top three podcast episodes, creating directories if needed, and saves audio files locally.
Dependencies: The project relies on the requests, xmltodict, and Apache Airflow libraries for efficient podcast data management.

![photo_2023-11-22_16-08-54](https://github.com/Ataa55/AirFlow-Download-Podcasts-Pipline-/assets/115408306/6ff94aee-0950-4a9c-8da8-eb4d6c97d54a)

To run the data pipeline, set up an Apache Airflow environment, configure the necessary connections in Airflow's web UI, and trigger the DAG execution. This project demonstrates expertise in data engineering and workflow automation, providing an efficient solution for podcast episode handling.

![photo_2023-11-22_16-08-32](https://github.com/Ataa55/AirFlow-Download-Podcasts-Pipline-/assets/115408306/6f0f55c8-cb32-4a95-9b7b-07c3aeacb39c)
