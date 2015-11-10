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
from colorama import init
import requests
import pafy
import time


class VideoCrawler:
	
	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.current_depth = 0
		self.depth_links = []
		self.videos = []

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

		best = video_obj.getbest()
		
		#print best.resolution



		"""
		create a CSV document for the data collected from the videos extracted
		"""	
		with open("video_data.csv", "a") as myfile:
    			myfile.write(video_obj.title + "," + video_obj.duration + ","  + best.resolution + "," + video_url + "\n")

		best.download(quiet=False)
	

		"""
		adds the prefix "http://www.youtube.com" to the url collected from the sidebar to complete the link
		these addresses will be where the crawler will go next.
		"""
		s = "http://www.youtube.com"
		new_list = [s + link for link in links]


		#for link in new_list:
			#print link


		video = Video( video_obj.title, uploader, new_list )
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
	response = "https://www.youtube.com/watch?v=ytNNG2yWi9Y"
else:
	#If using python version 3 change raw_input to input
	response = raw_input("Please enter starting YouTube URL: ")


#If using python version 3 change raw_input to input
user_depth = raw_input("Please enter the depth of the crawl: ")

crawler = VideoCrawler(response, user_depth)
crawler.crawl()


for video in crawler.videos:
	print video
		
		
