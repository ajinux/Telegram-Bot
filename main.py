import urllib
import os
import random
import telepot
import re
import requests
import GoogleApi
import library_login
from time import strftime,sleep

#Reference :https://core.telegram.org/bots/api
TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Telegram API token
IMG_NAME='none'
IMG_FILE='img_file.txt' #Name of the files that contains image
COUNT=0                 #no.of messages send
log_info=""
RE_BOOK=[] 

#Reference: http://unicode.org/emoji/charts/full-emoji-list.html
#unicode literals for emojis
smile=u'\U0001F601'
smile1=u'\U0001F600'
happy= u'\U0001F604'      #smiling face with open mouth and smiling eyes
love=u'\U0001F60D'        #smiling face with heart-shaped eyes
sad=u'\U0001F614'         #pensive face
done=u'\U0001F44D'        #thumbs up sign
confuse=u'\U0001F633'     #flushed face
birth_cake=u'\U0001F382'  #BIRTHDAY CAKE
balloon=u'\U0001F388'     #Balloon
book_open=u'\U0001F4D6'   #open book
books=u'\U0001F4DA'       #stack of books
cry=u'\U0001F622'         #crying face
rupee=u'\U000020B9'       #symbol rupee
hourglass=u'\U0000231B'   #HOURGLASS
loud_speaker=u'\U0001F4E2'#PUBLIC ADDRESS LOUDSPEAKER
smile_sun=u'\U0001F60E'   #SMILING FACE WITH SUNGLASSES
pointer=u'\U0001F449'     #backhand index pointing right

def send_quote(chat_id):

	#fetching name of the image
	global IMG_NAME
	img_file=open(IMG_FILE,'r')
	data=img_file.readlines()
	img_file.close()
	IMG_NAME=data[random.randint(0,len(data)-1)]
	
	#sending the image
	show_keyboard = {'keyboard': [['Like it'+love], ['Not Good'+sad]]}
	if IMG_NAME.endswith('.gif'):
		 bot.sendSticker(chat_id, open('xxxxx/'+IMG_NAME[0:len(IMG_NAME)-1], 'rb'))#xxxx=PATH of the image folder
		 bot.sendMessage(chat_id,'Good morning Ajith',reply_markup=show_keyboard)
		 return

	f=open('xxxxxx'+IMG_NAME[0:len(IMG_NAME)-1],'rb')
	bot.sendPhoto(chat_id,f,caption=get_greetings()+happy+'!',reply_markup=show_keyboard)
	
def delete_quote(chat_id):
	#remove the name of the file from the text file
	global IMG_NAME
	f = open(IMG_FILE,"r+")
	data = f.readlines()
	f.seek(0)
	for i in data:
		if i != IMG_NAME:
			f.write(i)
		else:
			del_file=open('delete_file.txt','a') 
			del_file.write(IMG_NAME)
			del_file.close()
			hide_keyboard={'hide_keyboard':True}
			response=bot.sendMessage(chat_id,'The photo has been successfully deleted from the database'+done,reply_markup=hide_keyboard)
	f.truncate()
	f.close()
	IMG_NAME='none'
	send_quote(chat_id) #to send another photo 

def send_jokes(chat_id,bool):

	img_list=os.listdir('xxxxxxxxxxxxxx') #PATH of the dir that contains the image
	img_name=img_list[random.randint(0,len(img_list)-1)]
	if img_name.endswith('.gif'):
		bot.sendSticker(chat_id, open('xxxxxxxx/'+img_name, 'rb'))
		return
	hide_keyboard={'hide_keyboard':True}
	if bool:
		bot.sendPhoto(chat_id,open('xxxxxxxxx/'+img_name, 'rb'),caption=get_greetings()+smile1,reply_markup=hide_keyboard)
		return
	bot.sendPhoto(chat_id,open('xxxxxxxxx/'+img_name, 'rb'),caption='Jokes for u'+smile1,reply_markup=hide_keyboard)

def get_greetings():
    #returns the greetings according to the current time
	time=int(strftime("%H"))
	if time<12 and time >2:
	   return 'Good morning Ajith'
	if time>=12 and time<=18:
		return 'Good afternoon Ajith'
	if time>=18 and time<=22:
		return 'Good evening Ajith'
	else:
		return 'Good night Ajith'

def fecth_library(chat_id,log):

	global log_info
	global RE_BOOK
	log_info=log 
	log_info=log_info.split()
     
	if len(log_info)==1:
		data=library_login.crawl_library()
	elif len(log_info)==2:
		data=library_login.crawl_library(log_info[1],log_info[1])
	elif len(log_info)==3:
		data=library_login.crawl_library(log_info[1],log_info[2])
	else:
		bot.sendMessage(chat_id,"Invalid input --Please Try again!")
		log_info=""
		return
	#data=["1 80369 S.Chand's Engineering Physics: Vol-II 21/1/2016 4/2/2016 BOOK ISSUE You have fine :242", '2 78556 Programming in C 18/2/2016 3/3/2016 BOOK ISSUE You have fine :186', '3 79113 Engineering Physics 1/6/2016 15/6/2016 BOOK RENEW']
	if type(data)!=list:
		bot.sendMessage(chat_id,data)
		log_info=''
		return  

	cleaned_data=[]

	for ele in data:
		sub=[]
		dates=re.findall('.*?([0-9]+/[0-9]+/[0-9]+)',ele)
		sub.append(dates[0])
		sub.append(dates[1])
		book=re.findall('(.*?)[0-9]+/[0-9]+/[0-9]+',ele[8:])
		sub.append(book[0])
		fine=re.findall('fine :([0-9]+)',ele)

		if len(fine)!=0:
		  sub.append(fine[0])

		cleaned_data.append(sub)
	
	temp=len(cleaned_data) #no of books taken
	msg="You have "+str(temp)
	if temp==1:
		msg=msg+" Book in your Account:"+books+"\n"
	else:
		msg=msg+" Books in your Account:"+books+"\n"
	#print msg
	RE_BOOK=[]
	key=[]
	flag=0

	for i in range(temp):
		msg=msg+"Book No : "+str(i+1)+"\nBOOK NAME  :"+cleaned_data[i][2]+book_open+"\nISSUED DATE :"+cleaned_data[i][0]+"\nDUE DATE      :"+cleaned_data[i][1]
		key.append(['Renew '+cleaned_data[i][2]])
		if len(cleaned_data[i])==4:
		  msg=msg+"\nFINE                :"+cleaned_data[i][3]+rupee+cry+"\n"
		else:
		  msg=msg+"\nFINE                : 0"+rupee+smile+"\n"
		  RE_BOOK.append([cleaned_data[i][2],cleaned_data[i][1]])#[book name,Due date]
		  flag=1
	
		show_keyboard={'keyboard':[['Set remainder!']]+key}
	else:
		show_keyboard={'keyboard':key}

	bot.sendMessage(chat_id,msg,reply_markup=show_keyboard)	

def handle(msg):
	content_type,chat_type,chat_id=telepot.glance(msg)

	print chat_id
	if chat_id!=229915721: #chat_id is always constant for a paticular user
		bot.sendMessage('Sorry '+msg['from']['first_name']+" this is Ajith kumar's personal bot --Access Denied!")
		return

	global COUNT
	COUNT=COUNT+1
	print "No.of Messages send :",COUNT	
	message=msg['text']
	
	if message=='Like it'+love and IMG_NAME!='none':
		  hide_keyboard={'hide_keyboard':True}
		  response=bot.sendMessage(chat_id,'Thank you'+smile,reply_markup=hide_keyboard)

	elif message=='Not Good'+sad and IMG_NAME!='none':
		  delete_quote(chat_id)

	elif message.lower()=='/birth':

		  tim=strftime("%Y-%m-%d")#Gives the current date
		  #tim="2016-06-10"
		  birth_list=GoogleApi.get_birthday(tim,tim)#FORMAT:tim=yy-mm-dd
		  if not birth_list:
			bot.sendMessage(chat_id,'Hey, Ajith none of your friends have birthday today'+smile)
			return

		  cnt=1 
		  names="TODAY'S BIRTHDAY"+birth_cake+balloon
		  for name in birth_list:
			  names=names+"\n"+str(cnt)+")"+name[:-11]+","
			  cnt=cnt+1


		  show_keyboard={'hide_keyboard':True}
		  bot.sendMessage(chat_id,names[:-1]+" "+happy,reply_markup=show_keyboard)

	elif message.lower().startswith('library'):

		  fecth_library(chat_id,message)

	elif message.startswith('Renew '):

		  global log_info
		  
		  if len(log_info)==1:
			  response=library_login.renew_library(message[6:])

		  elif len(log_info)==2:
			  response=library_login.renew_library(message[6:],log_info[1],log_info[1])

		  elif len(log_info)==3:
			  response=library_login.renew_library(message[6:],log_info[1],log_info[2])

		  else:
			  bot.sendMessage(chat_id,"Invalid credentials!--Please Try again")

		  hide_keyboard={'hide_keyboard':True}
		  bot.sendMessage(chat_id,response,reply_markup=hide_keyboard)
		  log_info=""

	elif message=='Set remainder!' and log_info!='' and RE_BOOK!='':
		  key=[]
		  for book in RE_BOOK:
			 key.append(['Remind on :'+book[0]+' - '+book[1]])
		  
		  show_keyboard={'keyboard':key}
		  bot.sendMessage(chat_id,'Choose a Book to set remainder'+smile,reply_markup=show_keyboard)

	elif message.startswith('Remind on :') and log_info!='' and RE_BOOK!='':
		  #message format :'Remind on :Introduction to Autonomous Mobile Robots - 16/6/2016'

		  book1=re.findall('^Remind on :(.*?) -',message)[0] 
		  date=re.findall('.*?([0-9]+/[0-9]+/[0-9]+)',message)[0]
		  hide_keyboard={'hide_keyboard':True}

		  if len(log_info)==1:
			roll_no='14bit004'
		  else:
			roll_no=log_info[1]
		  raw_data=date+' '+roll_no+' '+book1+'\n'
		  
		  f=open('remainder.txt','a+')
		  lines = f.readlines()
		
		  if raw_data in lines:
				bot.sendMessage(chat_id,'A remainder has been already set for book '+book1+' for roll no '+roll_no+' on '+date+smile,reply_markup=hide_keyboard)
				return

		  
		  f.write(raw_data) #raw_data='date roll_no book_name\n'
		  f.close()
		 
		  date=date.split('/') #date =09/06/2016
		  date=date[2]+'-'+date[1]+'-'+date[0]#Change the format of the date as according to the google calendar
		  #date =2016-06-09

		  print GoogleApi.create_remainder('Renew '+book1,date)
		  bot.sendMessage(chat_id,'Remainder set successfully! Will remind on the book Due date '+date+smile+' a remainder is also set in your google calendar!',reply_markup=hide_keyboard)
	
	elif message.lower()=='/youtube':

		  show_keyboard={'keyboard':[['channel:All'],['channel:Computerpile'],['channel:Vsauce'],['channel:veritasium'],['channel:Numberphile'],['channel:TedX']]}#Favorite youtube channels
		  bot.sendMessage(chat_id,"Please select a youtube channel"+happy+" or search for your favorite youtube channel as 'channel:<channel_name>'"+smile,reply_markup=show_keyboard)

	elif message.lower().startswith('channel:'):

		  result=GoogleApi.youtube_data(message[8:].encode('utf-8'))#message[8:]='channel_name'
		  hide_keyboard={'hide_keyboard':True}

		  if type(result)!=list:
			bot.sendMessage(chat_id,result+message[8:]+confuse,reply_markup=hide_keyboard)
			return

		  for data in result:
			bot.sendMessage(chat_id,'Channel Name:'+data[0]+smile1+'\nVideo Title  :'+data[1]+'\nwww.youtube.com/watch?v='+data[2],reply_markup=hide_keyboard)

	elif message.lower()=='/joke':

		  send_jokes(chat_id,True) #sends a joke pic

	elif message.lower()=='/quote':

		  send_quote(chat_id)  #sends a inspirational quote

	elif message.lower()=='/kct' or message.lower()=='/kctinfo':

		  response=urllib.urlopen('http://www.kct.ac.in/events')#For events at kct
		  resp=response.read() 
		  result=re.findall('<a href="http://www.kct.ac.in/events/(.+?)/"',resp)
		  result=[data.replace('-',' ') for data in result]  #will replace all the '-' symbols with blankspace

		  num=1
		  final_msg='EVENTS AT KCT'+hourglass+'\n'

		  for element in result[::2]:
			  final_msg=final_msg+str(num)+') '+element+'.'+happy+'\n'
			  num=num+1

		  final_msg=final_msg+'REFER :www.kct.ac.in/events'+'\n' 

		  response=urllib.urlopen('http://www.kct.ac.in/announcements') #For announcements at kct
		  resp=response.read()
		  result=re.findall('<a href="http://www.kct.ac.in/announcements/(.+?)/"',resp)
		  result=[data.replace('-',' ') for data in result]

		  num=1
		  final_msg=final_msg+'\n'+'ANNOUNCEMENTS AT KCT'+loud_speaker+'\n'

		  for element in result[::2]:
			  final_msg=final_msg+str(num)+') '+element+'.'+smile_sun+'\n'
			  num=num+1

		  final_msg=final_msg+'REFER :www.kct.ac.in/announcements'+'\n' 

		  hide_keyboard={'hide_keyboard':True}
		  bot.sendMessage(chat_id,final_msg,reply_markup=hide_keyboard)

	elif message.startswith('what is ') or message.startswith('pronounce '):

		  #reference :http://developer.wordnik.com/docs.html#!/word
		  api_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #wordnik API key

		  if message.startswith('what is '):#For defenitions
			  word=message[8:]
			  url='http://api.wordnik.com/v4/word.json/'+word+'/definitions?limit=3&includeRelated=true&sourceDictionaries=all&useCanonical=true&includeTags=false&api_key='+api_key 
			  resp=requests.get(url)
			  data=resp.json()  

			  if not data:
				  bot.sendMessage(chat_id,'Sorry Ajith no such word found!'+confuse)
				  return

			  word=data[0]['word'].upper()
			  final_msg="Defenition['"+word+"']:\n"

			  for element in data:
				  final_msg=final_msg+pointer+element['text']+'\n'

			  show_keyboard={'keyboard':[['pronounce '+word+happy]]}
			  bot.sendMessage(chat_id,final_msg,reply_markup=show_keyboard)

		  else:
			  url='http://api.wordnik.com:80/v4/word.json/'+message[10:]+'/audio?useCanonical=true&limit=50&api_key='+api_key
			  resp=requests.get(url)
			  data=resp.json()

			  try:
				url=data[0]['fileUrl'] 
			  except:  #If no such word found
				bot.sendMessage(chat_id,'Sorry Ajith no such word found!'+confuse)
				return

			  resp=requests.get(url) #Gets the audio file in binary format

			  word=data[0]['word'].upper()
			  file_name='pronounce_'+word+'.mp3'

			  with open(file_name,'wb') as audio:
				  audio.write(resp.content)
			  
			  hide_keyboard={'hide_keyboard':True}
			  bot.sendAudio(chat_id, open(file_name, 'rb'), title=word)
			  bot.sendMessage(chat_id,done,reply_markup=hide_keyboard)
			  os.remove(file_name)	#To remove the send file	

	elif message=='/help' or message=='/start':

              data='''COMMANDS AVAILABLE:
/joke   - Sends you a joke picture or gif
/kct    -Gives latest events and announcements at KCT
/youtube- Gives the latest videos of a youtube channel
/birth  -Gives a list of facebook friends birthday
/quote  -Gives an inspiration quote from great peoples
/help   -Gives the descriptions about this Bot 
library <user_id> <password> -to renew and set remainders
what is <word>        -to define the word
pronounce <word>      -will send you a pronunciation of the word 
                   '''
              bot.sendMessage(chat_id,data)

	else:
		  
		  bot.sendMessage(chat_id,'Upcoming a images for u '+msg['from']['first_name']+'!')
		  send_jokes(chat_id,False)
		  send_quote(chat_id)
		 


bot=telepot.Bot(TOKEN)

bot.message_loop(handle)

print "Listening..."

while 1:
   sleep(10)