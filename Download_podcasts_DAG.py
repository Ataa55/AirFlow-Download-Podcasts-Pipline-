from airflow.decorators import dag, task 
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook 
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pendulum
import requests
import xmltodict
import os
pdcasts_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
@dag(
    dag_id = "podcast_summary",
    schedule_interval="@daily",
    start_date = pendulum.datetime(2023,11,5),
    catchup= False
)
def podcast_summary():

    create_dbtask = PostgresOperator(
        task_id = "podcast_table_task",
        sql = r"""
                create table if not exists episodes(
                link text primary key,
                title text,
                filename text,
                published text,
                description text);
                """,
        postgres_conn_id = "podcasts_conn"
    )
    
    @task()
    def get_episodes():
       data = requests.get(pdcasts_URL)
       feed = xmltodict.parse(data.text)
       episodes = feed['rss']['channel']['item']
       print(f"your new episodes are {len(episodes)}")
       return episodes
    
    new_episodes = get_episodes()
    create_dbtask.set_downstream(new_episodes)

    @task 
    def load_apisodes(episodes):
        
        hook = PostgresHook(postgres_conn_id = "podcasts_conn")
        stored = hook.get_pandas_df("select * from episodes;")
        
        Updated_episodes = []

        for item in episodes:

            if item["link"] not in stored["link"].values:
                filename = f"{item['link'].split('/')[-1]}.mp3"
                Updated_episodes.append([item["link"], item["title"], item["pubDate"], item["description"], filename])

        hook.insert_rows(table="episodes", rows=Updated_episodes, target_fields=["link", "title","published", "description", "filename"]) 

    load_apisodes(new_episodes)

    @task
    def download_podcasts(episodes):

        for episode in episodes[:3]:
            filename = f"{episode['link'].split('/')[-1]}.mp3"
            podcast_path= os.path.join("podcasts", filename)
            os.makedirs("podcasts", exist_ok=True)

            if not os.path.exists(podcast_path):
                print(f"Downloading{filename}")
                data = requests.get(episode["enclosure"]["@url"])

                with open(podcast_path, "wb+") as f:
                    f.write(data.content)

    download_podcasts(new_episodes)

summary = podcast_summary()