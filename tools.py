import sys
import os
import readline
import time
from colorama import Fore,Style
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
from glob import glob
import shutil
import img2pdf
# from fpdf import FPDF

# Created by Defri Indra M
# 
# https://github.com/greyploiter
# 
# ==================================

try:
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
		pass

	def downloadImage(file_,dir_):
		print(f"\n{Fore.BLUE}[-] Loading to get Images ...{Style.RESET_ALL}")
		file = file_
		num = 0
		# print(file)
		for i in range(0,len(file)):
			numbers = f"{str(num).zfill(2)}"
			title = dir_+"/"+numbers+".jpg"
			if os.path.exists(title):
				continue
				pass
			# print(f"wget --no-check-certificate -q -nc {file[i]} -P {dir_}")
			os.system(f"wget --no-check-certificate -nc \"{file[i]}\" -q -O \"{title}\"")
			num += 1
			pass
		print(f"\n{Fore.GREEN}[+] Success to get image ....{Style.RESET_ALL}")
		pass

	def createDir(dir_):
		print(f"\n{Fore.BLUE}[-] Checking folder ....{Style.RESET_ALL}")
		time.sleep(1)
		if not os.path.exists(dir_):
			os.makedirs(dir_)
			print(f"\n{Fore.GREEN}[+] Created folder {dir_} ...{Style.RESET_ALL}")
		else:
			print(f"{Fore.YELLOW}\n[+] Folder {dir_} Exist ...{Style.RESET_ALL}")
			pass
		pass


	def createPdf(dir_):
		print(f"\n{Fore.BLUE}[-] Loading to created {dir_}.pdf ...{Style.RESET_ALL}")
		lenImages = glob(str(dir_)+"/*.jpg")
		lenImages.sort()
		imagesArr = []
		for imageLink in lenImages:
			imagesArr.append(f"\"{imageLink}\"")
			pass
		images = " ".join(image for image in imagesArr)
		convert2pdf = f"img2pdf {images} -o \"{dir_}.pdf\""
		os.system(convert2pdf)
		print("\r")
		print(f"\n{Fore.GREEN}[+] Success to created {dir_}.pdf ...{Style.RESET_ALL}")
		pass

	#  Kurang Efektif
	# def createPdf(dir__):
	# 	dir_ = dir__;
	# 	print(f"\n{Fore.BLUE}[-] Loading to created {dir_}.pdf ...{Style.RESET_ALL}")
	# 	images = list(glob(dir_+"/*.jpg"))
	# 	images.sort()
	# 	pdf = FPDF()
	# 	for image in images:
	# 		print(f"""
	# pdf.add_page()
	# pdf.image(\"{image}\",0,0,pdf.w,pdf.h)""")
	# 		pass
	# 	# pdf.output(dir_+".pdf")
	# 	print(f"\n{Fore.GREEN}[+] Success to created {dir_}.pdf ...{Style.RESET_ALL}")

	def deleteDir(dir_):
		print(f"\n{Fore.BLUE}[-] Prepare to remove {dir_} ...{Style.RESET_ALL}")
		# dir__ = "\""+dir_+"\""
		if os.path.exists(dir_):
			shutil.rmtree(dir_)
			print(f"{Fore.GREEN}\n[+] Completed Removing {dir_} ...{Style.RESET_ALL}")
			pass
		pass


	def main():
		chooseQ = int(input(f"[1] Single Link\n[2] Mass Link\n{Fore.RED}[?] Choose : {Style.RESET_ALL}"))
		if chooseQ == 1:
			link = input(f"{Fore.RED}Link Manga Indo {Style.RESET_ALL} : ")
			saveImageQ = input(f"\n{Fore.YELLOW}[?] Save images (y/n) ?? {Style.RESET_ALL}")
			bsoup = req(link)
			title = bsoup[1]
			linkImage = bsoup[0]
			if not os.path.exists(title+".pdf"):
				if title != "Halaman tidak di temukan - Mangaindo":
					createDir(title)
					downloadImage(linkImage,title)
					createPdf(title)
					if not saveImageQ == "y" or saveImageQ == "Y" :
						deleteDir(title)
						pass
				else:
					print(f"\n{Fore.RED}[+] {title} \n[+] Check Kembali Link{Style.RESET_ALL}")
					pass
			else:
				print(f"{Fore.RED}[+] {title}.pdf is exist {Style.RESET_ALL}")
				pass
			pass
		else:
			linkTxt = input(f"{Fore.RED}Link [txt] Manga Indo {Style.RESET_ALL} : ")
			saveImageQ = input(f"\n{Fore.YELLOW}[?] Save images (y/n) ?? ")
			# open file
			with open(linkTxt ,'r') as data:
				links = data.read()
				links = links.split("\n")
				for link in links :
					if len(link) < 1:
						continue
						pass
					bsoup = req(link)
					title = bsoup[1]
					linkImage = bsoup[0]
					if not os.path.exists(title+".pdf"):
						if title != "Halaman tidak di temukan - Mangaindo":
							createDir(title)
							downloadImage(linkImage,title)
							createPdf(title)
							if not saveImageQ == "y" or saveImageQ == "Y" :
								deleteDir(title)
								pass
						else:
							print(f"\n{Fore.RED}[+] {title} \n[+] Check Kembali Link{Style.RESET_ALL}")
							pass
					else:
						print(f"{Fore.RED}[+] {title}.pdf is exist {Style.RESET_ALL}")
						pass
					pass
				pass
			pass
		pass
except Exception as e :
		raise Exception(f"{Fore.RED} Error : {e} {Style.RESET_ALL}")
