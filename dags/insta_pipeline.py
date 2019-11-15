from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import HagLeadModule.get_HashTag as ht
import pandas as pd

args = {"owner": "HiSim", "start_date": days_ago(n=1)}
dag = DAG(dag_id="Insta_Pipline", default_args=args, schedule_interval="@daily")

url_scrapy_dir = "/Users/hyuninsim/airflow/insta_explorer"
data_scrapy_dir = "/Users/hyuninsim/airflow/insta_crawl"
# Bash Operator
insta_url_cmd = """s
        cd {}
        scrapy crawl insta_url -s FEED_URI='/Users/hyuninsim/airflow/data/insta_url/test_url.csv' -s FEED_FORMAT=csv 
        """.format(
    url_scrapy_dir
)

insta_data_cmd = """s
        cd {}
        scrapy crawl insta_data -s FEED_URI='/Users/hyuninsim/airflow/data/insta_data/test_data.csv' -s FEED_FORMAT=csv 
        """.format(
    data_scrapy_dir
)


def get_hashtag_module(**kwargs):
    print("collecting hash tags...")
    insta_data = ht.Extract_HashTag(pd.read_csv("./data/insta_data/test_data.csv"))
    result = insta_data.find_tags()
    return pd.DataFrame(result).head()


insta_url_crawling = BashOperator(
    task_id="insta_url_crawling", bash_command=insta_url_cmd, dag=dag
)

insta_data_crawling = BashOperator(
    task_id="insta_data_crawling", bash_command=insta_data_cmd, dag=dag
)

collecting_tag = PythonOperator(
    task_id="get_hashtag_module",
    provide_context=True,
    python_callable=get_hashtag_module,
    dag=dag,
)


# t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

# t2 = BashOperator(task_id="sleep", bash_command="sleep 3", dag=dag)

# t3 = BashOperator(task_id="print_whoami", bash_command="whoami", dag=dag)

# t1 >> t2 >> t3
