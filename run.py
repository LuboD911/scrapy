import os

if __name__ == "__main__":
    os.system("cmd /c scrapy crawl mangospider -O result.json:json")