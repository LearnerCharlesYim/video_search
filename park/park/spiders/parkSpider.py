from scrapy import Request
from scrapy.spiders import Spider
from park.items import ParkItem
import re
from selenium import webdriver

class parkSpider(Spider):
    name = "park"

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.currentPage = 1

    def start_requests(self):  # 初始请求
        url = "https://you.ctrip.com/travels/"
        yield Request(url)

    def parse(self, response):  # 解析函数
        list_selector = response.xpath("//div[@class='city']")
        print(len(list_selector))

        for one_selector in list_selector:
            try:
                city = one_selector.xpath("div[@class='city-sub']/a[1]/text()").extract()[0]
                url = one_selector.xpath("div[@class='city-sub']/a[2]/@href").extract()[0]
                name = one_selector.xpath("div[@class='city-sub']/a[2]/text()").extract()[0]
                author = one_selector.xpath("div[3]/p/a[2]/text()").extract()[0]
                day = one_selector.xpath("div[3]/p/i/text()").extract()[0]
                hot = one_selector.xpath("div[@class='city-sub']/p/i[1]/text()").extract()[0]

                item = ParkItem()
                item["name"] = name
                item["city"] = city
                item["hot"] = hot

                item["url"] = url
                item["author"] = author
                item["day"] = day
                yield item

    #             # 生成详细页请求
    #
    #             url = "https://you.ctrip.com" + one_selector.xpath("dl/dd/a/@href").extract()[0]
    #             item["intro"] = url
    #             # meta为字典，typePase为详细页解析函数
    #             yield Request(url,
    #                           meta={"item": item},
    #                           callback=self.typePase)

            except:
                pass
    #
    #         # # 获取下一页
    #         # self.currentPage += 1
    #         # if self.currentPage < round(int(maxPage) * 10000, 0):
    #         # # if self.currentPage < 3:
    #         #     nextUrl = "https://you.ctrip.com/searchsite/sight/?query=" + "%" + "e5" + \
    #         #               "%" + "85" + "%" + "ac" + "%" + "e5" + "%" + "9b" + "%" + \
    #         #               "ad&isAnswered=&isRecommended=&publishDate=&PageNo=%d"%self.currentPage
    #         #     yield Request(nextUrl)
    #
    # def typePase(self, response):  # 详细页解析函数
    #     try:
    #         appraise = \
    #             response.xpath("//body/div[3]/div[1]//div[1]/div[1]/ul/li[1]/span/b/text()").extract()[0]
    #     except:
    #         appraise = "0"
    #     try:
    #         location = response.xpath("//p[@class='s_sight_addr']/text()").extract()[0]
    #     except:
    #         location = "暂无开景区位置数据"
    #
    #     try:
    #         aaaaa = response.xpath("//ul[@class='s_sight_in_list']/li[1]/span[2]/text()").extract()[0]
    #     except:
    #         aaaaa = "暂无开景区等级数据"
    #
    #     try:
    #         phoneNumber = \
    #             response.xpath("//ul[@class='s_sight_in_list']/li[last()]/span[last()]/text()").extract()[0]
    #     except:
    #         phoneNumber = "暂无联系方式"
    #
    #     try:
    #         openTime = response.xpath("//dl[@class='s_sight_in_list']/dd/text()").extract()[0]
    #     except:
    #         openTime = "暂无开放时间数据"
    #
    #     item = response.meta["item"]
    #     item["appraise"] = appraise
    #     item["location"] = location
    #     item["aaaaa"] = aaaaa
    #     item["openTime"] = openTime
    #     item["phoneNumber"] = phoneNumber
    #
    #     # print(item)
    #     yield item
