#!/usr/bin/env bash
timestamp="$(date +%Y/%m/%d-%H:%M:%S)"
echo "Running scrape at $timestamp"
/usr/local/bin/scrapy crawl TMOScrapy
