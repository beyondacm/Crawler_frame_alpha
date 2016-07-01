# -*- coding:utf-8 -*-
#
# 2016-06-17

import os
import urllib2
import urllib
import random
import json
import re

import sys
from spider_tools import * 
from spider_get_method import * 


reload(sys)
sys.setdefaultencoding('utf-8')

# crawl the index pages 
def crawl_index_pages(PROXY_LIST, URL_LIST) :
    
    # URL_LIST_SIZE = len(URL_LIST)
    # print len(URL_LIST) 
    i = 0
    with open('./index_pages', 'w') as fout:
        
        crawled_urllist = []
        uncrawled_urllist = URL_LIST
        print len(uncrawled_urllist)
        

        try :
            
            while URL_LIST is not None : 

                current_url = uncrawled_urllist[0]
                proxy = random.choice(PROXY_LIST)
                html = spider_url_by_get(url=current_url, proxy=proxy, enable_proxy=True)
                    
                if html is not None :
                    clean_data = clear_markup(html)
                    
                    if clean_data.startswith('{"totalsize":"0"'): 
                        # pop the top url from the uncrawled_urllist
                        crawled_url = uncrawled_urllist.pop(0)
                        # push the crawled_url to the crawled_urllist
                        crawled_urllist.append(crawled_url)
                        
                        print str(proxy) + 'is accessible'
                        print len(uncrawled_urllist)
                        print i, current_url
                    
                    elif clean_data.startswith('{"totalsize"'):
                        # pop the top url from the uncrawled_urllist
                        crawled_url = uncrawled_urllist.pop(0)
                        # push the crawled_url to the crawled_urllist
                        crawled_urllist.append(crawled_url)
                        
                        i = i + 1
                        # handle if pageNum > 1 
                        handle_pageNum(current_url, clean_data)
                        
                        print str(proxy) + 'is accessible'
                        print len(uncrawled_urllist)
                        print i, current_url
                        fout.write(clean_data + '\n')
                    else :
                        print str(proxy) + 'is un-accessible'
            
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            handle_error(crawled_urllist, uncrawled_urllist)
        except :
            print 'Exception Failed'
        
        finally :
            handle_error(crawled_urllist, uncrawled_urllist)

def handle_error(crawled_urllist, uncrawled_urllist) : 
       
    with open('./Url/index_crawled', 'w') as index_crawled,\
        open('./Url/index_uncrawled', 'w') as index_uncrawled:  
                
            index_crawled.write( str( len(crawled_urllist) ) + '\n' )
            for item in crawled_urllist:
                index_crawled.write( str(item) + '\n' )                            
            
            index_uncrawled.write( str( len(uncrawled_urllist) ) + '\n' )
            for item in uncrawled_urllist:
                index_uncrawled.write( str(item) + '\n' )


        
# handle the pageNum 
def handle_pageNum(current_url, clean_data) :
    
    init_url = current_url.split('&')[0]
    
    with open('./Url/url_expand', 'a') as url_expand:    
        try :
            json_data = json.loads(clean_data)
            # print json_data
            page_count = int( json_data['pagecount'] ) 
            print str( page_count ) + 'pages'
            if page_count > 1 :
                for i in range(2, page_count+1):
                    concat_url = init_url + '&page=' + str(i)
                    url_expand.write(concat_url + '\n')
        except ValueError, e:
            
            print '--------' , str(e)
            # continue 
                    

def main():
    
    format_url(init_url='http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx?word=')
    URL_LIST = get_urllist()
    PROXY_LIST = get_proxylist()
    crawl_index_pages(PROXY_LIST, URL_LIST) 

if __name__ == '__main__':
    main()

