import scrapy
import datetime
import os
import csv
from time import strftime
from scrapy_splash import SplashRequest


class TmoscrapySpider(scrapy.Spider):
    name = "TMOScrapy"
    allowed_domains = ["192.168.12.1"]
    start_urls = ["http://192.168.12.1/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={"wait": 0.5})

    def parse(self, response):
        date_time = strftime("%Y-%m-%d %H:%M:%S")
        output_dir = "/data/"

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        pri_file = output_dir + "pri_signal.csv"
        sec_file = output_dir + "sec_signal.csv"

        pri_file_exists = os.path.isfile(pri_file)
        sec_file_exists = os.path.isfile(pri_file)

        # RSRP
        pri_rsrp = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[1]/mat-expansion-panel/div/div/div[1]/span/text()"
        ).get()
        pri_rsrp = pri_rsrp.split()[0]

        # SNR
        pri_snr = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[1]/mat-expansion-panel/div/div/div[2]/span/text()"
        ).get()
        pri_snr = pri_snr.split()[0]

        # RSRQ
        pri_rsrq = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[1]/mat-expansion-panel/div/div/div[3]/span/text()"
        ).get()
        pri_rsrq = pri_rsrq.split()[0]

        # RSSI
        pri_rssi = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[1]/mat-expansion-panel/div/div/div[4]/span/text()"
        ).get()
        pri_rssi = pri_rssi.split()[0]

        # Secondary
        # RSRP
        sec_rsrp = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[2]/mat-expansion-panel/div/div/div[1]/span/text()"
        ).get()
        sec_rsrp = sec_rsrp.split()[0]

        # SNR
        sec_snr = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[2]/mat-expansion-panel/div/div/div[2]/span/text()"
        ).get()
        sec_snr = sec_snr.split()[0]

        # RSRQ
        sec_rsrq = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[3]/div/div[2]/mat-accordion/div[2]/mat-expansion-panel/div/div/div[3]/span/text()"
        ).get()
        sec_rsrq = sec_rsrq.split()[0]

        # UPTIME
        uptime_h = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[1]/div/div/div[3]/div[10]/span[1]/text()"
        ).get()
        uptime_m = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[1]/div/div/div[3]/div[10]/span[2]/text()"
        ).get()

        uptime_s = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[1]/div/div/div[3]/div[10]/span[3]/text()"
        ).get()

        # VERSION
        version = response.selector.xpath(
            "/html/body/app-root/app-side-menu/mat-sidenav-container/mat-sidenav-content/app-overview/div[2]/div[1]/div/div/div[3]/div[8]/text()"
        ).get()

        # UPTIME
        time_str = "{}{}{}".format(uptime_h,uptime_m,uptime_s)
        uptime = datetime.datetime.strptime(time_str, '%Hh %Mm %Ss').time()

        with open(pri_file, "a") as csvfile:
            headers = ["DATE_TIME", "RSRP", "SNR", "RSRQ", "RSSI", "VERSION", "UPTIME"]
            pri_rows = [
                {
                    "DATE_TIME": date_time,
                    "RSRP": pri_rsrp,
                    "SNR": pri_snr,
                    "RSRQ": pri_rsrq,
                    "RSSI": pri_rssi,
                    "VERSION": version,
                    "UPTIME": uptime,
                }
            ]
            writer = csv.DictWriter(csvfile, headers)
            if not pri_file_exists:
                writer.writeheader()
            writer.writerows(pri_rows)

        with open(sec_file, "a") as csvfile:
            headers = ["DATE_TIME", "RSRP", "SNR", "RSRQ", "VERSION", "UPTIME"]
            sec_rows = [
                {
                    "DATE_TIME": date_time,
                    "RSRP": sec_rsrp,
                    "SNR": sec_snr,
                    "RSRQ": sec_rsrq,
                    "VERSION": version,
                    "UPTIME": uptime,
                }
            ]
            writer = csv.DictWriter(csvfile, headers)
            if not sec_file_exists:
                writer.writeheader()
            writer.writerows(sec_rows)
