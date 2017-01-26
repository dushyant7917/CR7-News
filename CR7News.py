from Tkinter import *

import requests
from bs4 import BeautifulSoup

agent = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

def get_news():
	GoalNews = []

	req = requests.get("http://www.goal.com/en-india", headers=agent)
	soup = BeautifulSoup(req.content,"html.parser")

	for i in soup.find_all("span", attrs = {'itemprop': 'name', 'class': 'title'}):
		if i.text not in GoalNews:
			GoalNews.append(i.text)

	for i in soup.find_all("span", attrs = {'itemprop': 'headline', 'class': 'title'}):
		if i.text not in GoalNews:
			GoalNews.append(i.text)

	for i in soup.find_all("h4", attrs = {'itemprop': 'name', 'class': 'headline'}):
		if i.text not in GoalNews:
			GoalNews.append(i.text)

	return GoalNews

def fill_listbox():
	RemovedNews = []
	with open('RemovedNews.db', 'r') as fl:
		for line in fl:
			RemovedNews.append(line.replace("\n", ""))

	fl.close()

	for news in get_news():
		NewsTitle = news.split(" ")
		for word in NewsTitle:
			if word == "CR7" or word.lower() == "cristiano" or word.lower() == "ronaldo":
				if news not in listbox.get(0, END) and news not in RemovedNews:
					listbox.insert(0, news)

root = Tk()
root.geometry("600x400")
root.title("CR7 News!")
img = PhotoImage("photo", file="icon.png")
root.tk.call('wm', 'iconphoto', root._w, img)

def Button1():
	with open('News.db', 'w') as fl:
		for news in listbox.get(0, END):
			fl.write(news + "\n")

	fl.close()

def Button2():
	with open('RemovedNews.db', 'a') as fl:
		fl.write(listbox.get(ANCHOR) + "\n")

	fl.close()

	listbox.delete(ANCHOR)

	with open('News.db', 'w') as fl:
		for news in listbox.get(0, END):
			fl.write(news + "\n")

	fl.close()

def Button3():
	fill_listbox()

	with open('News.db', 'w') as fl:
		for news in listbox.get(0, END):
			fl.write(news + "\n")

	fl.close()


label1 = Label(root, text="Latest News About Cristiano Ronaldo", bg="black", fg="white")

listbox = Listbox(root)

button2 = Button(root, text = "Remove", command = Button2)
button3 = Button(root, text = "Refresh", command = Button3)

label1.pack(fill=X)
listbox.pack(fill=BOTH, expand=1)
button3.pack(fill=X, side=LEFT, expand=1)
button2.pack(fill=X, side=LEFT, expand=1)

try:
	RemovedNews = []
	with open('News.db', 'r') as fl, open('RemovedNews.db', 'r') as rf:
		for line in fl:
			RemovedNews.append(line.replace("\n", ""))

		for news in fl:
			if news not in RemovedNews:
				listbox.insert(END, news.replace("\n", ""))

	fl.close()
	rf.close()

except:
	pass

fill_listbox()
with open('News.db', 'w') as fl:
	for news in listbox.get(0, END):
		fl.write(news + "\n")

fl.close()

root.mainloop()
