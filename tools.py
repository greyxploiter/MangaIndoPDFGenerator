import sys
import os
import time
from colorama import Fore,Style
import requests
from bs4 import BeautifulSoup as bs
from fpdf import FPDF
import urllib.request
from glob import glob

# Created by Defri Indra M
# 
# https://github.com/greyploiter
# 
# ==================================



def req(link):
	req = requests.get(link)
	bsReq = bs(req.content,"html.parser")
	file = []
	for parsePage in bsReq.find_all("meta",attrs={'property':'og:image'}):
		file.append(parsePage.get("content"))
		pass
	for eachs in bsReq.find_all("meta",attrs={'property':'og:title'}):
		title = eachs.get("content")
		pass
	print(f"\n[+] Scanning {Fore.GREEN}{link}{Style.RESET_ALL} Completed ... ")
	return file,title

def downloadImage(file_,dir_):
	print(f"\n{Fore.BLUE}[-] Loading to get Image ...{Style.RESET_ALL}")
	file = file_
	dir_ = "\""+dir_+"\""
	# print(file)
	for i in range(0,len(file)):
		os.system(f"wget -q -nc {file[i]} -P {dir_}")
		pass
	print(f"\n{Fore.GREEN}[+] Success to get image ....{Style.RESET_ALL}")

def createDir(dir_):
	print(f"\n{Fore.BLUE}[-] Checking folder ....{Style.RESET_ALL}")
	time.sleep(1)
	if not os.path.exists(dir_):
		os.makedirs(dir_)
		print(f"\n{Fore.GREEN}[+] Created folder {dir_} ...{Style.RESET_ALL}")
	else:
		print(f"{Fore.YELLOW}\n[+] Folder {dir_} Exist ...{Style.RESET_ALL}")
		pass


def createPdf(dir__):
	dir_ = dir__;
	print(f"\n{Fore.BLUE}[-] Loading to created {dir_}.pdf ...{Style.RESET_ALL}")
	images = list(glob(dir_+"/*.jpg"))
	images.sort()
	pdf = FPDF()
	for image in images:
		pdf.add_page()
		pdf.image(image,0,0,pdf.w,pdf.h)
		pass
	pdf.output(dir_+".pdf")
	print(f"\n{Fore.GREEN}[+] Success to created {dir_}.pdf ...{Style.RESET_ALL}")


def main():
	link = input(f"{Fore.RED}Link Manga Indo {Style.RESET_ALL} : ")
	bsoup = req(link)
	title = bsoup[1]
	linkImage = bsoup[0]
	createDir(title)
	downloadImage(linkImage,title)
	createPdf(title)