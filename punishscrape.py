import requests
import string
import random
import mysql.connector

email = "email@provider.net"
passwd = "password"

baseurl = "http://myuservault.com/"

s = requests.Session()

useragents = ["Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Android; Mobile; rv:29.0) Gecko/29.0 Firefox/29.0",
"Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
"Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/34.0.1847.18 Mobile/11B554a Safari/9537.53",
"Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53"]

headers = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-us,en;q=0.5\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nKeep-Alive: 115\r\nConnection: keep-alive\\Cookie: disclaimer_accepted=true"
headers = headers.split("\r\n")

useragent = random.choice(useragents)
#cookies = dict(disclaimer_accepted='true')

s = requests.Session()
s.headers.update({'User-Agent': useragent})

def login(email, passwd):
	s.get("http://punishtube-members.com/members/")
	request = s.post("http://punishtube-members.com/members/", data={"username": email, "password": passwd})
	#print request.text
	return request.url

def getBetween(first, last, fullstring):
	after = fullstring.split(first)
	items = []
	i = 0
	for between in after:
		#if i > 0:
		inner = between.split(last)[0]
		items.append(inner)
		#++i
	return items

def getInfo(url, links = False):
	request = s.get(url)
	if links == False:
		alldata = ["http://myuservault.com/videos_categories.php"]
	else:
		alldata = links
	i = 0
	for x in alldata:
		if links == False:
			currenturl = x
		else:
			currenturl = x["link"]
		request = s.get( currenturl )
		requestbody = request.text
		out = []
		allurls = getBetween('data-location="', '"', requestbody)
		allthumbs = getBetween('style="background-image:url(', '.jpg', requestbody)
		try:
			allvidthumbs = getBetween('<source src="', '" type="video/mp4">', requestbody)
		except:
			allvidthumbs = False
		allnames = getBetween('<p class="name">', "</p>", requestbody)
		for y in range(1, len(allurls)):
			try:
				out.append({"name": allnames[y], "link": baseurl + allurls[y] + "&ipp=100", "thumb": allthumbs[y]+".jpg", "vidthumb": allvidthumbs[y]})
				#print str(i) + ": " + allnames[y] + ' ' + allvidthumbs[y]
			except:
				out.append({"name": allnames[y], "link": baseurl + allurls[y] + "&ipp=100", "thumb": allthumbs[y]+".jpg"})
				#print str(i) + ": " + allnames[y]
			i = i + 1
	return out
	# http://myuservault.com/videos_categories.php
	# return all nID's as an associative array thing with names

def getMP4(url):
	info = s.get(baseurl + url).text
	try:
		videolink = getBetween('		        file: "', '",', info)[1]
		videothumb = getBetween('		        image: "', '",', info)[1]
		videoviews = getBetween('<p>', '</p>', info)[1]
		videodesc = getBetween('<p>', '</p>', info)[2]
		return [videolink, videothumb, videoviews, videodesc]
	except: return False

starturl = login(email, passwd)
categories = getInfo(starturl)
videos = getInfo(starturl, categories)

for d in categories:
	pass

for x in videos:
	print x["link"]
	mp4 = getMP4(x["link"])
	if mp4 != False:
		print mp4[0]
		#print x["name"] + ": " + mp4[3] + "\n" + x["thumb"] + '\n' + x['vidthumb'] + "\n\n"
