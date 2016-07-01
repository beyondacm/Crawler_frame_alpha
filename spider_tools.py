# -*- coding:utf-8 -*-
# Tools function for spider
# 2016-06-17
import os
import random
import re

from spider_get_method import * 
from itertools import izip

# Function  Preview :
# clear_markup()
# ping_ip()
# remove_from_list()
# format_url()
# init_proxy_pools()
# get_proxylist()
# get_urllist()
# proxy_redetect() 


# clear the markup of the crawled data
def clear_markup(html=None) :
    
    if html is None:
        return None
    else :
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', html)
        return cleantext

# test a ip whether can be use by ping 
def ping_ip(ip=None):
    
    ping_cmd = 'ping -c 2 -W 5 %s' %ip
    ping_result = os.popen(ping_cmd).read()
    print 'ping_cmd : %s, ping_result : %r' %(ping_cmd, ping_result)

    if ping_result.find('100% packet loss') < 0:
        print 'ping %s ok' % ip
        return True
    else :
        print 'ping %s fail' % ip
        return False

# remove element from a list
def remove_from_list(item, origin_list) :
    
    origin_list.remove(item)
    print 'removing ' + str(item) + ',' + str( len(origin_list) )

# format the initial urls 
def format_url(fin='../CN_Dict/words.dic', fout='./Url/url_pools', init_url=None):
    
    if init_url is None :
        print 'init_url is None'
        return 

    with open(fin, 'r') as words_dic, \
        open(fout, 'w') as url_pool:
            
            for words in words_dic:
                concat_url = init_url + words.strip() + "&page=1"
                url_pool.write(concat_url + '\n')

# append to url_list 
def get_urllist( url_pools='./Url/url_pools' ):
    
    URL_LIST = []
    with open(url_pools, 'r') as url_pools:
        URL_LIST = [ url.strip() for url in url_pools.readlines() ]
    
    return URL_LIST


# append to proxy_list
def get_proxylist( proxy_pools = './Proxy/proxy_pools' ):

    PROXY_LIST = []
    
    with open(proxy_pools, 'r') as proxy_pools:
        for line in proxy_pools:
            ip_info = line.strip().strip('{').strip('}')
            # print ip_info
            key = ip_info.split(': ')[0].strip("'")
            value = ip_info.split(': ')[1].strip("'")
            # print key, value
            ip_dict = {key:value}
            PROXY_LIST.append(ip_dict)

    return PROXY_LIST
    
# initial proxy_pools
def init_proxy_pools(proxy_pools, \
        IP='./Proxy/IP', \
        Port='./Proxy/Port', \
        Type='./Proxy/Type'):
    with open(IP, 'r') as IP, \
        open(Port, 'r') as Port, \
        open(Type, 'r') as Type, \
        open(proxy_pools, 'a') as proxy_pools:
            for line1, line2, line3 in izip(IP, Port, Type):
                key = line3.strip().lower()
                if key.startswith('http'):
                    value = line3.strip().lower() + '://' \
                            + line1.strip() + ':' + line2.strip()
                    
                    format_url = {key:value}
                    # print format_url
                    proxy_pools.write( str(format_url) + '\n')


# detect if ip can be used , if can append to ip_pools
def proxy_redetect(proxy_pools='./Proxy/proxy_pools', PROXY_LIST=None):
    
    init_proxy_pools(proxy_pools)
    PROXY_LIST = get_proxylist()

    if PROXY_LIST is None:
        print 'PROXY_LIST is None'
        return None
    else :
        # re detect if the ip can be used  
        os.remove(proxy_pools)
     
    # print proxy
    with open(proxy_pools,'a') as proxy_pools:
        for proxy in PROXY_LIST:
            for key in proxy :
                # print key
                value = proxy[key]
                print key, value
            # print value 
            ip = value.split("//")[1].split(":")[0].strip()
            
            ping_url = 'http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx?word=%E8%AE%BD&page=1'
            
            # with open(proxy_pools, 'a') as proxy_pools:
            if ping_ip(ip) :
                if spider_url_by_get(url=ping_url, \
                        proxy=proxy, enable_proxy=True) is not None:
                    print ip + 'is accessible'
                    proxy_pools.write(str(proxy) + '\n')
                else :
                    print ip + 'is un-accessible'
    
    # return True



