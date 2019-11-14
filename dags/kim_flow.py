from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import time, os
from pprint import pprint

import KimsModule.News_Collection as kim
import KimsModule.News_data_preprocessing as kim_pre
import KimsModule.Topic_Modeling_LDA_TF_IDF as kim_model
import pandas as pd


args = {"owner": "HiSim", "start_date": days_ago(n=1)}

dag = DAG(dag_id="kims_flow", default_args=args, schedule_interval="@daily")


def news_collect_module(**kwargs):
    print("Collecting News..")
    print("current:", os.getcwd())

    News = kim.News_Collect(["핀테크", "레그테크", "인슈어테크"], "2017-01-01", "2017-08-31")
    news = News.news_collect()

    return news.to_csv(
        "data/news_data/news_key_words_add.csv", encoding="utf-8", index=False,
    )


# /Users/hyuninsim/airflow/data
def data_preprocessing_module(**kwargs):
    print("data_preprocessing")
    print("WTFFFFF:", os.getcwd())
    ori_news = pd.read_csv("data/news_data/news_key_words_add.csv", encoding="utf-8")
    print("total Length: ", len(ori_news))
    NEWS = kim_pre.News_PreProcessing(ori_news)
    news = NEWS.tokens_ngram("./data/news_data/news_key_words_add_ngram.csv")
    return news.head(2)


def data_modeling_module(**kwargs):
    print("Data_modeling...")
    news = pd.read_csv(
        "data/news_data/news_key_words_add_ngram.csv",
        encoding="utf-8",
        lineterminator="\n",
    )
    news = news.dropna()
    news = news.reset_index()
    del news["index"]
    print("MODELING!!!! Length:", len(news))
    new_doc_ls = news["tokens"].to_list()
    DF = kim_model.Topic_LDA_TF_IDF(new_doc_ls)
    ldamodel = DF.LDA_TF_IDF(15)
    return ldamodel


collecting_t = PythonOperator(
    task_id="news_collect_module",
    provide_context=True,
    python_callable=news_collect_module,
    dag=dag,
)

preprocessing_t = PythonOperator(
    task_id="data_preprocessing_module",
    provide_context=True,
    python_callable=data_preprocessing_module,
    dag=dag,
)

modeling_t = PythonOperator(
    task_id="data_modeling_module",
    provide_context=True,
    python_callable=data_modeling_module,
    dag=dag,
)

collecting_t >> preprocessing_t >> modeling_t
