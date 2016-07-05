import feedparser

data = feedparser.parse('https://www.mailinator.com/feed?to=3868c3d9b25efcd8167b353aaeb1c4')

if len(data['entries']) > 0:
	cmd = data['entries'][0]['title_detail']['value']
	print cmd