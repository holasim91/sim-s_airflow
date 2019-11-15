# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import urllib.request
import datetime as dt
import pandas as pd
import csv

from insta_crawl.items import InstaCrawlItem


class InstaDataSpider(scrapy.Spider):
    name = "insta_data"
    allowed_domains = ["www.instagram.com"]
    start_urls = []
    url_dir = "../../data/insta_url/"
    csvname = "test_url"

    df = pd.read_csv("/Users/hyuninsim/airflow/data/insta_url/" + csvname + ".csv")
    for each_url in df["each_url"]:
        print("each_url : " + each_url)
        shortcode = each_url.split('"')[3]
        start_urls.append("https://www.instagram.com/p/" + shortcode + "/?__a=1")

    def __init__(self):
        self.number = 0

    def parse(self, response):
        self.number += 1
        print("response.url : " + response.url)
        each_json_data = json.loads(response.body)

        print("each_json_data : " + str(each_json_data))

        item = InstaCrawlItem()
        item["each_url"] = response.url

        url = each_json_data["graphql"]["shortcode_media"]["display_url"]

        try:
            urllib.request.urlretrieve(url, f"{self.number}.png")
        except:
            pass

        # item['each_location'] = each_json_data['data']['shortcode_media']['location']['name']
        # item['address_json'] = each_json_data['data']['shortcode_media']['location']['address_json']
        try:
            item["text"] = each_json_data["graphql"]["shortcode_media"][
                "edge_media_to_caption"
            ]["edges"][0]["node"]["text"]
        except:
            pass

        list_a = []
        try:
            for each in each_json_data["graphql"]["shortcode_media"][
                "edge_media_to_parent_comment"
            ]["edges"]:
                list_a.append(each["node"]["text"])
        except:
            pass

        item["hash_tag"] = list_a
        item["idx_name"] = self.number

        yield item
