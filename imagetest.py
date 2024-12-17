from icrawler.builtin import BingImageCrawler
import os

labels = ["Rabbits"]

for label in labels:
    path = "/Users/bannotaito/Spotify/images" + label
    crawler = BingImageCrawler(storage={'root_dir': path})
    crawler.crawl(keyword=label, max_num=500)


