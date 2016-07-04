# -*- coding:utf-8 -*-
#
# 2016-06-17

import urllib
import urllib2

USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"                
]


# 使用代理访问网站 - POST方式实现
def spider_url_by_post(url, data, proxy=None, enable_proxy=False):
    
    # make a string with 'POST'  
    method = 'POST'
    
    # create a handler 
    proxy_handler = urllib2.ProxyHandler(proxy)
    null_proxy_handler = urllib2.ProxyHandler({}) 
    
    # create an openerdirector instance according to enable_proxy
    if enable_proxy:
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies, proxy_handler, urllib2.HTTPHandler)
        print 'without using proxy to crawl pages'
    else :
        opener = urllib2.build_opener(null_proxy_handler)
        print 'using proxy to crawl pages'
    
    # install opener 
    urllib.install_opener(opener)
    
    # buidl a request 
    #data = urllib.urlencode(dictionary_of_POST_fiels_or_None)
    data = urllib.urlencode(data)
    request = urllib2.Request(url, data=data) 
    
    # Ramdom choose the user_agent 
    #user_agent = random.choice(USER_AGENT_LSIT)
    user_agent = USER_AGENT_LIST[1] 
    request.add_header('User-Agent', user_agent)
    request.get_method = lambda:method

    try :
        connection = opener.open(request, timeout=5)
        if connection.code == 200:
            html = connection.read()
            return html
        #else if connection.code == 403:
        #   return None
    except urllib2.HTTPError, ex:
        # print e.code, e.reason
        print 'spider_url_by_get（） -------- ', str(ex)
        # connection = ex
        return None
    except urllib2.URLError, ex:
        # print e.reason
        # print e.code, e.reason
        print 'spider_url_by_get（） -------- ', str(ex)
        remove_proxy(proxy)
        return None
    except Exception, ex:
        print 'spider_url_by_get（） -------- ', str(ex)
        remove_proxy(proxy)
        return None