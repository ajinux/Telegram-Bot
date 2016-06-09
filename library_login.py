from selenium import webdriver
from selenium.common import exceptions
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys

display = Display(visible=0, size=(800, 600))
display.start()

def crawl_library(username="14bit004",passwd="xxxxxxxx"):

	driver=webdriver.Firefox()
	#driver=webdriver.PhantomJS(executable_path=r'/usr/bin')
	#driver.set_window_size(0,0)
	
	try:
	
		driver.set_page_load_timeout(10)
		driver.get("http://10.1.105.24/opac/login.asp?user_id="+username+"&pwd="+passwd+"&log=Login&id=ON")
	except exceptions.TimeoutException:
		driver.close()
		return "sorry, library site is temporarily down!"
	try:
		driver.find_element_by_xpath(".//*[@id='AutoNumber2']/tbody/tr[1]/td[1]/font/b")
	except exceptions.NoSuchElementException:
		driver.close()
		return "Invaild username or password!--Please try again!"
	
	try:
		driver.find_element_by_xpath(".//*[@id='AutoNumber2']/tbody/tr[4]/td/font/b/font/font/a").click()
        #-----------------------------------------------------------------
		#FOR REFERENCE:
		#.//*[@id='AutoNumber2']/tbody/tr[4]/td/font/b/font/font--no books
		#.//*[@id='AutoNumber2']/tbody/tr[4]/td/font/b/font/font/a
        #-------------------------------------------------------------------
	except exceptions.NoSuchElementException:
		driver.close()
		if username=='14bit004':
		  return "Hi Ajith, You don't have any books your library account!"
		return username+" have no books in his/her library account"
		#--------------------------------------------------------------------
        #FOR REFERENCE:
	    #.//*[@id='table10']/tbody/tr/td/span/font/form  --2 books
	    #.//*[@id='table10']/tbody/tr/td/span/font/form  --1books
        #html=driver.page_source  --TO get the page source of the entire page
        #---------------------------------------------------------------------

	details=driver.find_element_by_xpath(".//*[@id='table10']/tbody/tr/td/span/font/form/table[1]")
	
	driver.close()
	return details.text.encode('utf-8')[56:].split('\n')
	


def renew_library(book_name,username="14bit004",passwd="Telebot"):
	 
	driver=webdriver.Firefox()
	#driver.set_window_size(0,0)
	
	try:
	
		driver.set_page_load_timeout(10)
		driver.get("http://10.1.105.24/opac/login.asp?user_id="+username+"&pwd="+passwd+"&log=Login&id=ON")
	except exceptions.TimeoutException:
		driver.close()
		return "sorry, library site is temporarily down!"

	try:
		driver.find_element_by_xpath(".//*[@id='AutoNumber2']/tbody/tr[4]/td/font/b/font/font/a").click()
		
	except exceptions.NoSuchElementException:
		 driver.close()
		 return "You have no books in library!"

	
	for row in range(2,10):
		try:
		 book=driver.find_element_by_xpath(".//*[@id='table10']/tbody/tr/td/span/font/form/table[1]/tbody/tr["+str(row)+"]/td[3]")
		except exceptions.NoSuchElementException:
			return "sorry, something went wrong! Try again"
		if book.text.encode('utf-8')==book_name:
			break


	driver.find_element_by_xpath(".//*[@id='table10']/tbody/tr/td/span/font/form/table[1]/tbody/tr["+str(row)+"]/td[8]/input").click()
	driver.find_element_by_xpath(".//*[@id='table10']/tbody/tr/td/span/font/form/center/img").click()
	alert=driver.switch_to_alert()
	alert.accept()
	response=driver.find_element_by_xpath(".//*[@id='table10']/tbody/tr/td/span/font/p[2]/table[2]/tbody/tr[2]/td[2]")
	driver.close()
	return response.text.encode('utf-8')

'''
#-----------------------------------------------------------------------------------------------------
# Tried to implement birthday wish option with '/birth' command
# but due to lack of facebook graph api support for writing any message
# on friends timeline, given a try with selenium but unfortunately
# the code is not generic --so, let it as it is for future reference.
#-----------------------------------------------------------------------------------------------------
def birthday_wish(name):
	driver=webdriver.Firefox()
	driver.set_page_load_timeout(10)
	driver.get('https://www.facebook.com/events/birthdays?ref=110')
	driver.find_element_by_xpath(".//*[@id='email']").send_keys('xxxxxxxx')
	driver.find_element_by_xpath(".//*[@id='pass']").send_keys('xxxxxxxxx')
	driver.find_element_by_xpath(".//*[@id='loginbutton']").click()

	try:
		details=driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]").text.encode('utf-8').split('\n')[2:]
	except exceptions.TimeoutException:       #html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]
		driver.close()
		return "sorry, Some error occured"

	details=[x for x in details if x!='View Friendship' and not x.endswith('years old')]
	print details
	if name in details:
		row=details.index(name)
		try:
		   driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div["+str(row+2)+"]/div/div/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div/textarea").send_keys("Wish you many more happy returns of the day")
		except exceptions.NoSuchElementException:
		   driver.close()
		   return "sorry, Some error occured"
		driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div["+str(row+2)+"]/div/div/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div/textarea").send_keys(Keys.ENTER)
		driver.close()
		return "Wished "+name+" successfully on his timeline"+u'\U0001F601'


	try:
		details=driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]").text.encode('utf-8').split('\n')[2:]
	except exceptions.NoSuchElementException: #html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]
		driver.close()
		return "sorry, Some error occured"

	details=[x for x in details if x!='View Friendship' and not x.endswith('years old')]
	print details
	if name in details:
		row=details.index(name)
		try:
		   driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div["+str(row+1)+"]/div/div/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div/textarea").send_keys("Wish you many more happy returns of the day")
		except exceptions.NoSuchElementException:
		   driver.close()
		   return "sorry, Some error occured"
		driver.find_element_by_xpath("html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div["+str(row+1)+"]/div/div/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div/textarea").send_keys(Keys.ENTER)
		driver.close()
		return "Wished "+name+" successfully on his timeline"+u'\U0001F601'

'''

#print renew_library("13bee077","Introduction to Autonomous Mobile Robots")
#print crawl_library('14bit0044')

