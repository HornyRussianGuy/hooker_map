#!/usr/bin/env bash
cd "${0%/*}/.."

scrapy crawl escort-europe | ./collector.py &
#scrapy crawl escort-europe | ./collector.py &
#scrapy crawl happyescorts  | ./collector.py &

wait

