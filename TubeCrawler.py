"""
Auther: David Corrigan 
www.hourglassapplications.com
d-corrigan@stny.rr.com

This webcrawler is designed to crawl YouTube and download random videos.
There is a sleep timer (around line 43) that slows the crawl down to avoid detection from YouTube.
** There is no waranty or guarantee that this will continue to work from day to day 
or that you wont get blackballed by YouTube.
This program requires pafy, requests & lxml which can be installed using pip from www.python.org

I am in no way responsible for illegal or mischievious use of this program 
Use at your own risk.
 

"""


from lxml import html
import BeautifulSoup
import requests
import pafy
import time
import csv
import random



class VideoCrawler:
	
	def __init__(self, starting_url, depth, duration):
		self.starting_url = starting_url
		self.depth = depth
		self.current_depth = 0
		self.duration = duration
		self.depth_links = []
		self.videos = []

	@staticmethod
	def get_sec(s):
    	 l = s.split(':')
    	 return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

	def crawl(self):


		video = self.get_video_from_link(self.starting_url)
		self.videos.append(video)

		self.depth_links.append(video.links)

		while self.current_depth < self.depth:
			current_links =[]
			for link in self.depth_links[self.current_depth]:
				current_video = self.get_video_from_link(link)
				current_links.extend(current_video.links)
				self.videos.append(current_video)


				#SLEEP TIMER added to avoid getting blackballed by YouTube
				time.sleep(5)

				#max_time = int(raw_input(duration))
				#start_time = time.time()  # remember when we started
		
				#if (time.time() - start_time) > max_time: 
					#print (Ctrl-Z)

					

			self.current_depth += 1
			self.depth_links.append(current_links)

		return

	def get_video_from_link(self,link):
		start_page = requests.get(link)
		tree = html.fromstring(start_page.text)

		"""
		this is where we parse the html to retreive certain tagged items using xpath 
		"""

		name = tree.xpath('//div[@class=" yt-card yt-card-has-padding"]//*/span[@class="watch-title "]/text()')[0]
		uploader = tree.xpath('//div[@class="yt-user-info"]/a/text()')[0]
		video_url = tree.xpath('//div[@class="watch-main-col "]/link[@itemprop="url"]/@href')[0]
		links = tree.xpath('//div[@class="watch-sidebar-body"]//*/a/@href') 

		#print name.strip()
		#print uploader
		#print video_url


		video_obj = pafy.new(video_url)
		print "Video Title: " + video_obj.title
		#print video_obj.description
		#print video_obj.duration
		#print video_obj.length

		sec = video_obj.duration
		print "Duration:" + str(self.get_sec(sec)) + " in seconds."

		best = video_obj.getbest(preftype="mp4")
		
		#print best.resolution

		no_comma_title = video_obj.title.replace(",", " ")
		
		foo = ["https://www.youtube.com/watch?v=COKlObhGt50", "https://www.youtube.com/watch?v=ZyvhnHzfGac", 
		"https://www.youtube.com/watch?v=esVZxjLrwH0", "https://www.youtube.com/watch?v=fOQ9svAVE7U", 
		"https://www.youtube.com/watch?v=xAg7z6u4NE8","https://www.youtube.com/watch?v=q-gYcvipozY",
		"https://www.youtube.com/watch?v=jnshSRAIFW0","https://www.youtube.com/watch?v=ni4V-kN0LMI",
		"https://www.youtube.com/watch?v=bbA2sYeUiSE","https://www.youtube.com/watch?v=S3Q_oyOWzHA",
		"https://www.youtube.com/watch?v=Y6XPUCMbf_E","https://www.youtube.com/watch?v=OGebiWgEkOw",
		"https://www.youtube.com/watch?v=KS0ooghAfag","https://www.youtube.com/watch?v=6eWDgNrLYps",
		"https://www.youtube.com/watch?v=waL5Cf-CFJU","https://www.youtube.com/watch?v=G6uQ8EyxMO0",
		"https://www.youtube.com/watch?v=wMuNjnNyaiA","https://www.youtube.com/watch?v=d82DmbYeAuI",
		"https://www.youtube.com/watch?v=Cts3MrHnYIU","https://www.youtube.com/watch?v=1H_XqO5OwWM",
		"https://www.youtube.com/watch?v=i_twGzgSq74"]

		response = random.choice(foo)


		"""
		create a CSV document for the data collected from the videos extracted
		"""	

		too_long = int(self.get_sec(sec)) < 600

		with open("video_data.csv", "a") as myfile:
			with open('video_data.csv', 'rt') as f:
	    		 reader = csv.reader(f, delimiter=',')
	     		 for row in reader:
	          		if no_comma_title.encode('utf-8') == row[0]: # if the username shall be on column 0 (-> index 2)
							self.duration += 1
							too_long = True;

							if self.duration % 5 == 0 :
								crawler = VideoCrawler(response, 50, 5000)
								crawler.crawl()
	              	 else:

	              	 	if too_long == True:
							with open("video_data.csv", "a") as myfile:
									myfile.write(no_comma_title.encode('UTF-8', 'ignore') + ","+ uploader.encode('UTF-8') + "," + video_obj.duration.encode('UTF-8') + ","  + best.resolution.encode('UTF-8') + "," + video_url.encode('UTF-8') + "\n")
						
							try:
								if too_long == True:
									best.download(quiet=False)
							except Exception as e:
								print ( "<p>Error: %s</p>" % str(e) )

		"""
		adds the prefix "http://www.youtube.com" to the url collected from the sidebar to complete the link
		these addresses will be where the crawler will go next.
		"""
		s = "http://www.youtube.com"
		new_list = [s + link for link in links]

		#remove duplicates
		myList = sorted(set(new_list))

		#for link in myList:
			#print link


		video = Video( video_obj.title, uploader, myList )
		self.videos.append(video)

		return video

class Video:

	def __init__(self, name,  uploader, links ):
	 	self.name = name
	 	self.uploader = uploader
	 	self.links = links

	def __str__(self):
        	return ("Name: " + self.name.encode('UTF-8') + 
        	"\r\nUploader: " + self.uploader.encode('UTF-8') + "\r\n")

print "\r\n"
print "-------------------------------------------------------------------"
print "Welcome to TubeCrawler"
print "Written by David Corrigan"
print "\n"
print "NOTICE:  Changing the starting URL will avoid duplicates from previous runs"  
print "NOTICE:  The depth of the crawl will EXPONENTIONALY increase the output"  
print "(example depth 0 may output 8 videos where depth 1 may output 64)"  
print "-------------------------------------------------------------------"
print "\r\n"

#If using python version 3 change raw_input to input
yes_or_no = raw_input("Would you like to use the default starting URL:  [y or n] ")

if yes_or_no == 'y':
	foo = ["https://www.youtube.com/watch?v=Ej6A7euo2K8", "https://www.youtube.com/watch?v=0in9XQkiVuA", 
	"https://www.youtube.com/watch?v=JZ9EsfAJatU", "https://www.youtube.com/watch?v=nn_Z4fKizVM", 
	"https://www.youtube.com/watch?v=xAg7z6u4NE8","https://www.youtube.com/watch?v=joBmbh0AGSQ",
	"https://www.youtube.com/watch?v=OGebiWgEkOw"]

	response = random.choice(foo)
else:
	#If using python version 3 change raw_input to input
	response = raw_input("Please enter starting YouTube URL: ")


#If using python version 3 change raw_input to input
user_depth = raw_input("Please enter the depth of the crawl: ")

#If using python version 3 change raw_input to input
#duration = raw_input("Please enter the duration in seconds: ")

duration = 5000

crawler = VideoCrawler(response, user_depth, duration)
crawler.crawl()


for video in crawler.videos:
	print video
		
		
