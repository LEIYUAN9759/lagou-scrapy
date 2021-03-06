import scrapy
import json
import math
import time


from tutorial.items import LaGou


class SfSpider(scrapy.Spider):
    name = "lagou"
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0"
    handle_httpstatus_list = [404]

    # allowed_domains = ["lagou.com"]

    def __init__(self):
        self.fail_urls = []

    def start_requests(self):
        # return [scrapy.FormRequest(str(self.url), callback=self.get_jobs, formdata={'kd': 'web前端'})]
        for i in range(1, 31):
            istrue = 'true' if i == 1 else 'false'
            formdata = {'first': istrue, 'pn': str(i), 'kd': 'web前端'}
            yield scrapy.FormRequest(str(self.url), callback=self.parseJson, formdata=formdata)

    def get_jobs(self, response):
        jsonjobs = json.loads(response.body_as_unicode())['content']['positionResult']
        page_num = math.ceil(jsonjobs['totalCount'] / jsonjobs['resultSize'])
        print('------------------------------------------------')
        print(page_num)
        time.sleep(1)

        for i in range(1, page_num):
            istrue = 'true' if i == 1 else 'false'
            formdata = {'first': istrue, 'pn': str(i), 'kd': 'web前端'}
            yield scrapy.FormRequest(str(self.url), callback=self.parseJson, formdata=formdata)

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        print('---------------------------------------parse---------------------------------------')

    def parseJson(self, response):
        print('============res===========')
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        # print(response)
        jsonresponse = json.loads(response.body_as_unicode())
        # print(jsonresponse)
        for sel in jsonresponse['content']['positionResult']['result']:
            item = LaGou()
            item['salary'] = sel['salary']
            item['company'] = sel['companyFullName']
            item['financeStage'] = sel['financeStage']
            item['workYear'] = sel['workYear']
            item['industryField'] = sel['industryField'].split(",")
            yield item
