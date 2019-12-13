import re,json
import requests
from download import *
def create_user_dir(username):
    foldername = "pinterest_downloads/pinterest_" + username
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    return foldername
def get_data(pinid,page=10):
	dir=create_user_dir(pinid)
	html=requests.get("https://www.pinterest.com/pin/{}/".format(pinid)).text
	ok=str(re.findall('<script id="initial-state" type="application/json">(.*?)</script>',html)[0])
	data=["https://i.pinimg.com/originals/"+n for n in re.findall('"url":"https://i.pinimg.com/originals/(.*?)"',ok)]
	book=json.loads(ok)["resourceResponses"][1]["options"]['bookmarks'][0]
	p=json.loads(ok)["resourceResponses"][1]["options"]['pin']
	if book:
		is_next=True
	for runing in range(int(page)):
		url='https://in.pinterest.com/resource/RelatedPinFeedResource/get/?data={"options":{"bookmarks":["'+book+'"],"isPrefetch":false,"field_set_key":"base_grid","pin":"'+p+'","prepend":false,"search_query":"","context_pin_ids":[],"source":"deep_linking","top_level_source":"deep_linking","top_level_source_depth":1},"context":{}}'
		ss=json.loads(requests.get(url).text)
		for n in ss["resource_response"]["data"]:
			data.append(n["images"]["orig"]["url"])
		book=ss["resource"]["options"]['bookmarks'][0]
		p=ss["resource"]["options"]['pin']
		if book =="-end-":
			is_next=False
	return data,dir

if __name__=="__main__":
	# pinno="432275264234547854"
	pinno=str(input("Enter Pin Number -->"))
	print("Collecting Images")
	data,path=get_data(pinno)
	img=[]
	for n in data:
		if n not in img:
			img.append(n)
	print("Downloading Started")
	c=1
	for n in img:
		print("Process: [{}/{}] {}".format(c,len(img),n.split("/")[-1]),end="\r")
		Download(urlinit=n,location=path)
		c+=1
	print("Downloading Completed {}".format(len(img)))
	input()