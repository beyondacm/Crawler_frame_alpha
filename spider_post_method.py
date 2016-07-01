# -*- coding:utf-8 -*-
#
# 2016-06-30

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
