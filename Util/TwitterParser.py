from BeautifulSoup import BeautifulSoup
import urllib2
import re

html = urllib2.urlopen('https://twitter.com/dmcsec')
soup = BeautifulSoup(html)

tweet = soup.find('meta', {'name': 'description'})['content']

print re.findall(r'"(.*?)"', tweet)[0]
