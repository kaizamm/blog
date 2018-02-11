---
layout:       post
title:        "scrapy-爬虫-基础"
date:         2018-01-31 12:00:00
categories: document
tag:
  - python
  - scrapy
---

* content
{:toc}

### 前言
爬虫实现方式有很多，可选择的语言也很多，如node.js、java、python；对于python，实现的方式也有很多；可以直接用requests模块请求到网页数据后，用正则/xpath/css去匹配，涉及到的模块有bs4/urllib/urlencode/etree等；现在用scrapy模块，帮我们省去了数据获取的工作，我们只需要对数据进行清洗过滤即可，“伟人是站在巨人肩头的侏儒”，正所谓“工欲善其事，必先得其器”。Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。
### 工程搭建
直接上官网 https://scrapy.org/ 和
http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html
#### 环境
+ Python 2.7 or Python 3.4+
+ install
```bash
pip install scrapy
```
>另外插一句，pip和conda的区别，自行百度吧; 关于scrapy有两种部署模式，部署到本地和部署到cloud；本次只记录本地

#### 编写spider
+ 对于response数据过滤两种方式:xpath/css

用css表达式:

```python
# myspider.py
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
```
运行
```bash
root@kaiz-virtual-machine:/opt# scrapy runspider myspider.py
2018-01-31 15:17:42 [scrapy.utils.log] INFO: Scrapy 1.5.0 started (bot: scrapybot)
2018-01-31 15:17:42 [scrapy.utils.log] INFO: Versions: lxml 4.1.1.0, libxml2 2.9.7, cssselect 1.0.3, parsel 1.3.1, w3lib 1.18.0, Twisted 17.9.0, Python 2.7.12 (default, Nov 20 2017, 18:23:56) - [GCC 5.4.0 20160609],
...
2018-01-31 17:24:17 [scrapy.core.scraper] DEBUG: Scraped from <200 https://blog.scrapinghub.com/page/11/>
{'title': u'Scrapy 0.12 released'}
2018-01-31 17:24:17 [scrapy.core.scraper] DEBUG: Scraped from <200 https://blog.scrapinghub.com/page/11/>
{'title': u'Spoofing your Scrapy bot IP using tsocks'}
...
```

对于以上spider用xpath写为:

```python
import scrapy
class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.xpath("//h2[@class='entry-title']/a/text()").extract():
            yield {'title': title}
        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
```

### 编写第一个爬虫(Spider)
现在开始用创建项目方式来爬虫，一般分为以下几个步骤：
+ 创建一个scrapy项目
+ 定义提取的Item
+ 编写爬取网站的spider并提取Item
+ 编写Item Pipeline来存储提取到的Item(即数据)

#### 创建项目
在开始爬取之前，需创建一个项目：
```bash
scrapy startproject tutorial
```
+ scrapy.cfg: 项目的配置文件
+ tutorial/: 该项目的python模块。之后您将在此加入代码。
+ tutorial/items.py: 项目中的item文件.
+ tutorial/pipelines.py: 项目中的pipelines文件.
+ tutorial/settings.py: 项目的设置文件.
+ tutorial/spiders/: 放置spider代码的目录.

#### Item
爬取的主要目的就是从非结构性的数据源提取结构性数据；类似orm，或是java的实体类一样
```python
import scrapy
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
```

#### spider
Spider类定义了如何爬取某个(或某些)网站。包括了爬取的动作(例如:是否跟进链接)以及如何从网页的内容中提取结构化数据(爬取item)。最后，由spider返回的item将被存到数据库(由某些 Item Pipeline 处理)或使用 Feed exports 存入到文件中。 换句话说，Spider就是您定义爬取的动作及分析某个网页(或者是有些网页)的地方。是用户编写用于从一个单一的网站或是一类网站爬取到的数据的类，需继承scrapy.Spider类，有以下三个属性
+ name:用于区别Spider,惟一
+ allowed_domains： 可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
+ start_urls： 目标url列表
+ start_requests()： 该方法的默认实现是使用 start_urls 的url生成Request。当spider启动爬取并且未制定URL时，该方法被调用。 当指定了URL时，make_requests_from_url() 将被调用来创建Request对象。 该方法仅仅会被Scrapy调用一次，因此您可以将其实现为生成器。该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。
如果您想要修改最初爬取某个网站的Request对象，您可以重写(override)该方法。 例如，如果您需要在启动时以POST登录某个网站，你可以这么写:
```python
def start_requests(self):
    return [scrapy.FormRequest("http://www.example.com/login",
                               formdata={'user': 'john', 'pass': 'secret'},
                               callback=self.logged_in)]
def logged_in(self, response):
    # here you would extract links to follow and return Requests for
    # each of them, with another callback
    pass
```
+ make_requests_from_url(url):该方法接受一个URL并返回用于爬取的 Request 对象。 该方法在初始化request时被 start_requests() 调用，也被用于转化url为request。默认未被复写(overridden)的情况下，该方法返回的Request对象中， parse() 作为回调函数，dont_filter参数也被设置为开启。 (详情参见 Request).
+ parse()： 是Spider的一个方法。被调用时，每个初始URL完成下载后生成的response对象会作为唯一参数传递给该函数。该方法负责解析返回的数据(response data),提取数据生成item及生成需进一步处理的URL的requset对象。以下dmoz_spider.py:
+ log(message[, level, component])
使用 scrapy.log.msg() 方法记录(log)message。 log中自动带上该spider的 name 属性。 更多数据请参见 Logging 。

样例一：
```python
import scrapy
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ['dmoz.org']
    start_urls = [
        "http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html",
         "http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/feed-exports.html"
    ]
    def parse(self,response):
        filename = response.url.split('/')[-2]
        with open(filename,'wb') as f:
            f.write(response.body)
```

样例二：
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]
    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
```

样例三：另一个在单个回调函数中返回多个Request以及Item的例子:
```python
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```

#### 爬取规则(Crawling rules)
当编写爬虫规则时，请避免使用 parse 作为回调函数。 由于 CrawlSpider 使用 parse 方法来实现其逻辑，如果 您覆盖了 parse 方法，crawl spider 将会运行失败。link_extractor 是一个 Link Extractor 对象。 其定义了如何从爬取到的页面提取链接。callback 是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中每获取到链接时将会调用该函数。该回调函数接受一个response作为其第一个参数， 并返回一个包含 Item 以及(或) Request 对象(或者这两者的子类)的列表(list)。
http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spiders.html


```
scrapy crawl dmoz
'''
2018-01-31 19:34:39 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2018-01-31 19:34:40 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://scrapy-chs.readthedocs.io/robots.txt> (referer: None)
2018-01-31 19:34:40 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/feed-exports.html> (referer: None)
2018-01-31 19:34:44 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html> (referer: None)
'''
```

### Selectors选择器
当抓取网页时，你做的最常见的任务是从HTML源码中提取数据。现有的一些库可以达到这个目的：

这里给出XPath表达式的例子及对应的含义:
+ BeautifulSoup
是在程序员间非常流行的网页分析库，它基于HTML代码的结构来构造一个Python对象， 对不良标记的处理也非常合理，但它有一个缺点：慢
+ lxml 是一个基于 ElementTree (不是Python标准库的一部分)的python化的XML解析库(也可以解析HTML)。

Scrapy提取数据有自己的一套机制。它们被称作选择器(seletors)，因为他们通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分。

XPath 是一门用来在XML文件中选择节点的语言，也可以用在HTML上。 CSS 是一门将HTML文档样式化的语言。选择器由它定义，并与特定的HTML元素的样式相关连。xpath语法详见http://www.runoob.com/xpath/xpath-syntax.html ;

```bash
XPath Expression	Result
/bookstore/book[1]	Selects the first book element that is the child of the bookstore element
/bookstore/book[last()]	Selects the last book element that is the child of the bookstore element
/bookstore/book[last()-1]	Selects the last but one book element that is the child of the bookstore element
/bookstore/book[position()<3]	Selects the first two book elements that are children of the bookstore element
//title[@lang]	Selects all the title elements that have an attribute named lang
//title[@lang='en']	Selects all the title elements that have a "lang" attribute with a value of "en"
/bookstore/book[price>35.00]	Selects all the book elements of the bookstore element that have a price element with a value greater than 35.00
/bookstore/book[price>35.00]/title	Selects all the title elements of the book elements of the bookstore element that have a price element with a value greater than 35.00
```
+ /html/head/title: 选择HTML文档中 <head> 标签内的 <title> 元素的selector
+ /html/head/title/text(): 选择上面提到的 <title> 元素的文字
+ //td: 选择所有的 <td> 元素
+ //div[@class="mine"]: 选择所有具有 class="mine" 属性的 div 元素
+ extract() : To actually extract the textual data, you must call the selector .extract() method
Scrapy选择器构建于 lxml 库之上，这意味着它们在速度和解析准确性上非常相似。

##### 构造选择器(selectors)
Scrapy selector是以 文字(text) 或 TextResponse 构造的 Selector 实例。 其根据输入的类型自动选择最优的分析方法(XML vs HTML):
```python
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
#以文字构造:
>>> body = '<html><body><span>good</span></body></html>'
>>> Selector(text=body).xpath('//span/text()').extract()
[u'good']
# 以response构造:
>>> response = HtmlResponse(url='http://example.com', body=body)
>>> Selector(response=response).xpath('//span/text()').extract()
[u'good']
#为了方便起见，response对象以 .selector 属性提供了一个selector， 您可以随时使用该快捷方法:
>>> response.selector.xpath('//span/text()').extract()
[u'good']
```

#### 在shell中尝试selector选择器
HTML源码:
```html
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
```
首先, 我们打开shell:
```bash
scrapy shell 'http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html'
```
接着，当shell载入后，您将获得名为 response 的shell变量，其为响应的response， 并且在其 response.selector 属性上绑定了一个selector。

+ response.body
+ response.headers
+ response.selector:当输入response.selector时，将获取到一个可以用于查询数据的selector选择器，以及映射到response.selector.xpath()、response.selector.css()的快捷方法shortcut:response.xpath()和response.css()
+ response.url

可用的Scrapy对象

Scrapy终端根据下载的页面会自动创建一些方便使用的对象，例如 Response 对象及 Selector 对象(对HTML及XML内容)。

这些对象有:
+ crawler - 当前 Crawler 对象.
+ spider - 处理URL的spider。 对当前URL没有处理的Spider时则为一个 + Spider 对象。
+ request - 最近获取到的页面的 Request 对象。 您可以使用 replace() 修+ 改该request。或者 使用 fetch 快捷方式来获取新的request。
+ response - 包含最近获取到的页面的 Response 对象。
+ sel - 根据最近获取到的response构建的 Selector 对象。
+ settings - 当前的 Scrapy settings


我们构建一个XPath来选择title标签内的文字:
```python
>>> response.selector.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]
```
由于在response中使用XPath、CSS查询十分普遍，因此，Scrapy提供了两个实用的快捷方式: response.xpath() 及 response.css():
```python
>>> response.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]
>>> response.css('title::text')
[<Selector (text) xpath=//title/text()>]
```
如你所见， .xpath() 及 .css() 方法返回一个类 SelectorList 的实例, 它是一个新选择器的列表。这个API可以用来快速的提取嵌套数据。

为了提取真实的原文数据，你需要调用 .extract() 方法如下

```python
>>> response.xpath('//title/text()').extract()
[u'Example website']
```

现在我们将得到根URL(base URL)和一些图片链接:

```python
>>> response.xpath('//base/@href').extract()
[u'http://example.com/']

>>> response.css('base::attr(href)').extract()
[u'http://example.com/']

>>> response.xpath('//a[contains(@href, "image")]/@href').extract()
[u'image1.html',
 u'image2.html',
 u'image3.html',
 u'image4.html',
 u'image5.html']

>>> response.css('a[href*=image]::attr(href)').extract()
[u'image1.html',
 u'image2.html',
 u'image3.html',
 u'image4.html',
 u'image5.html']

>>> response.xpath('//a[contains(@href, "image")]/img/@src').extract()
[u'image1_thumb.jpg',
 u'image2_thumb.jpg',
 u'image3_thumb.jpg',
 u'image4_thumb.jpg',
 u'image5_thumb.jpg']

>>> response.css('a[href*=image] img::attr(src)').extract()
[u'image1_thumb.jpg',
 u'image2_thumb.jpg',
 u'image3_thumb.jpg',
 u'image4_thumb.jpg',
 u'image5_thumb.jpg']
```
#### 结合正则表达式使用选择器(selectors)
```python
>>> response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
[u'My image 1',
 u'My image 2',
 u'My image 3',
 u'My image 4',
 u'My image 5']
```

#### 使用相对XPaths
记住如果你使用嵌套的选择器，并使用起始为 / 的XPath，那么该XPath将对文档使用绝对路径，而且对于你调用的 Selector 不是相对路径。

比如，假设你想提取在 <div> 元素中的所有 <p> 元素。首先，你将先得到所有的 <div> 元素:
```python
>>> divs = response.xpath('//div')
```
开始时，你可能会尝试使用下面的错误的方法，因为它其实是从整篇文档中，而不仅仅是从那些 <div> 元素内部提取所有的 <p> 元素:
```python
>>> for p in divs.xpath('//p'):  # this is wrong - gets all <p> from the whole document
...     print p.extract()
```
下面是比较合适的处理方法(注意 .//p XPath的点前缀):
```python
>>> for p in divs.xpath('.//p'):  # extracts all <p> inside
...     print p.extract()
```
另一种常见的情况将是提取所有直系 <p> 的结果:
```python
>>> for p in divs.xpath('p'):
...     print p.extract()
```
### 可用的工具命令
scrapy提供了两种类型的命令。一种必须在scrapy项目中运行，别外一种是全局的
+ 全局命令
  - startproject
  - settings 例如获取项目名称：scrapy settings --get BOT_NAME
  - runspider:这个命令和crawl命令的区别在于crawl命令后是spider的name，而runspider命令后加的是爬虫的文件名，在本文的项目中，使用crawl命令：scrapy crawl baidu; 使用runspider就是：scrapy runspider baidu.py
  - shell
  - fetch: --nolog/--headers/--no-redirect 分别是不输出日志信息，返回网页的请求头和禁止重定向。如果网页没有重定向的话返回的还是原网页。
  使用Scrapy下载器(downloader)下载给定的URL，并将获取到的内容送到标准输出。 scrapy fetch --nolog http://www.example.com/some/page.htm
  - view: 这个命令比较有用，它的作用是请求网址，输出网址的源码，并将该网页保存成一个文件，使用浏览器打开。如果打开的网址和你正常加载的网页有所不同，一般情况下没显示的部分使用了异步加载。因此该命令可以用来检查 spider 所获取到的页面,并确认这是您所期望的。
  - version: 这个命令可以查询当前scrapy的版本，和一些依赖库版本信息。
+ 项目命令
  - crawl: 使用spider进行爬取 scrapy crawl myspider
  - check: 运行contract检查 scrapy check [-l] <spider>
  - list: 列出当前项目中所有可用的spider。每行输出一个spider。scrapy list
  - edit: 使用 EDITOR 中设定的编辑器编辑给定的spider语法: scrapy edit <spider>; 如果你不使用vim作为编辑器的话，这个命令不常用，因为这个命令会调用vim来编辑文件。
  - parse: 获取给定的 URL 并使用相应的 spider 分析处理。如果您提供 --callback 选项,则使用 spider 的该方法处理,否则使用 parse
  - genspider:在spiders目录下创建最基本的模版，scrapy genspider baidu www.baidu.com
  ```bash
  scrapy genspider -l
  '''
  Available templates:
  basic
  crawl
  csvfeed
  xmlfeed
  '''
   scrapy genspider -d basic
   scrapy genspider -t basic example example.com
  ```

  - deploy
  - bench

### 还有什么?
到此你已经从网页上抓到了你想要的一些数据,但这仅仅冰山一角.scrapy还提供了更为强大的特性使得爬虫更为简单,如:
+ html,xml源数据选择及提取内置支持
+ 提供了一系列在spider之间共享的可复用的过滤器,即Item Loaders. 对智能处理爬取数据提供了内置支持
+ 通过feed导出提供了多种格式JSON,CSV,XML. 多存储后端FTP,S3,本地文件系统的支持
+ 提供了media pipeline,可以自动爬取到的数据中的图片或其他资源
+ 高可扩展性,你可以通过使用signals,设计好的API(中间件,extensions,pipelines)来定制你的功能.
+ 内置中间件及扩展为下列功能提供了支持
  - cookies and session处理
  - HTTP压缩
  - HTTP认证
  - user-agent模拟
  - robots.txt
  - 爬取深度限制
+ 针对非英语系中不标准或者错误的编码声明，提供了自动检测以健壮的编码支持
+ 支持根据模板生成爬虫。在加速爬虫创建同时，保持在大型项目中的代码更为一致。详细内容见genspider命令 http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#std:command-genspider
+ 针对多爬虫下性能评估、失败检测，提供了可扩展的状态收集工具
+ 提供交互式shell终端，为您测试xpath表达式、编写和调试爬虫提供了极大的方便
+ 提供system service，简化在生产环境的部署及运行
+ 内置web service使您可以监视及控制您的机器
+ 内置telnet终端，通过在scrapy进程中钩入python终端，例您可以查看并且调试爬虫
+ Logging为您在爬取过程中捕捉错误提供了方便
+ 支持sitemaps爬取
+ 具有缓存的DNS解析器
