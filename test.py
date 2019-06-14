__author__ = 'Lee'
import random
ip_pool = [
    '119.98.44.192:8118',
    '111.198.219.151:8118',
    '101.86.86.101:8118',
]
def ip_proxy():
    ip = ip_pool[random.randrange(0,3)]
    proxy_ip = 'http://'+ip
    proxies = {'http':proxy_ip}
    return proxies
c=ip_proxy()
print(type(c))
