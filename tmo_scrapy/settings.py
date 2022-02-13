BOT_NAME = "tmo_scrapy"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) Safari/537.36"

SPIDER_MODULES = ["tmo_scrapy.spiders"]
NEWSPIDER_MODULE = "tmo_scrapy.spiders"

ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
}

SPLASH_URL = "http://splash:8050/"

DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"
