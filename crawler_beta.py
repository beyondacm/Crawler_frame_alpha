# -*- coding:utf-8 -*-
#
# 2016-06-17

import random
import json
import sys
import os

from spider_get_method  import *  
from spider_post_method import * 
from spider_tools import * 

reload(sys)
sys.setdefaultencoding('utf-8')


# PROXY_LIST = []
# URL_LIST = []

cur_path = os.path.abspath(os.path.join( os.path.dirname(__file__)) )


# if error occurs, write the breakpoint infomation into files
def handle_error(crawled_urllist, uncrawled_urllist):
    # print current_path
    with open( cur_path + '/Data/crawled', 'w' ) as crawled :
        crawled.write( str( len(crawled_urllist)) + '\n' )
        for item in crawled_urllist :
            crawled.write( str(item) + '\n')
        
    with open( cur_path + '/Data/uncrawled', 'w') as uncrawled :
        uncrawled.write( str( len(uncrawled_urllist)) + '\n')
        for item in uncrawled_urllist:
            uncrawled.write( str(item) + '\n')


# handle the pageNum
def handle_pageNum(current_url, clean_data ) :

    init_url = current_url.split('&')[0]

    with open(cur_path + '/Data/url_expand', 'a') as url_expand:

        try :
            json_data = json.loads(clean_data)
            # print json_data
            page_count = int( json_data['pagecount'] )
            print str( page_count ) + 'pages'
            if page_count > 1:
                for i in range(2, page_count+1):
                    concat_url = init_url + '&page=' + str(i)
                    url_expand.write(concat_url + '\n')
        
        except ValueError, e:
            
            print '--------' , str(e)


def crawl_pages(PROXY_LIST, URL_LIST, data_pools) :

    i = 0
    with open( data_pools , 'a') as fout:

        crawled_urllist = []
        uncrawled_urllist = URL_LIST
        print len(uncrawled_urllist)
        
        try :

            while URL_LIST is not None:

                current_url = uncrawled_urllist[0]
                proxy = random.choice(PROXY_LIST)
                html = spider_url_by_get(url = current_url, \
                                        proxy = proxy, \
                                        enable_proxy = True)
                if html is not None:
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
                        handle_pageNum(current_url, clean_data )
                        
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
            print 'Finally'
            handle_error(crawled_urllist, uncrawled_urllist)

def main():
    
    PROXY_LIST = []
    URL_LIST = []

    URL_LIST = get_urllist(cur_path + '/Url/url_pools_0.txt')    
    PROXY_LIST = get_proxylist(cur_path + '/Proxy/ip_pools.txt')
    
    data_pools = cur_path + '/Data/data_pools.txt'
    crawl_pages(PROXY_LIST, URL_LIST, data_pools)



if __name__ == '__main__':
    main()


