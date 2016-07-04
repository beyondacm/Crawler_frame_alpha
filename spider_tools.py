# -*- coding:utf-8 -*-
#
# 2016-06-17

import re
import os 


# get URL_LIST from url_pools
def get_urllist(url_pools):

	URL_LIST = []
	with open(url_pools, 'r') as url_pools:
		URL_LIST = [ url.strip() for url in url_pools.readlines() ]

	return URL_LIST

# get PROXY_LIST from proxy_pools
def get_proxylist(proxy_pools):

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

# clear the markup of the crawled data
def clear_markup(html) :
    
    if html is None:
    	return None  
    else :
	    cleanr = re.compile('<.*?>')
	    cleantext = re.sub(cleanr, '', html)
	    return cleantext

# remove the useless proxy from PROXY_LIST
def remove_proxy(proxy) :
    PROXY_LIST.remove(proxy)
    print 'removing proxy :'+ str( len(PROXY_LIST) )


def ping_ip(ip=None):
    
#     ping_cmd = 'ping -c 2 -w 5 %s' % ip   
#     ping_result = os.system(ping_cmd)
#     print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
#     
#     if ping_result == 0:
#         print 'ping %s ok' % ip
#         return True
#     else:
#         print 'ping %s fail' % ip
         
    ping_cmd = 'ping -c 2 -W 5 %s' %ip     
    ping_result = os.popen(ping_cmd).read()
    print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
    
    # with open('./ip_pool_accessible.txt', 'a') as fout:
    if ping_result.find('100% packet loss') < 0:
        print 'ping %s ok' % ip
        # fout.write(ip + '\n')
        return True
    else:
        print 'ping %s fail' % ip



