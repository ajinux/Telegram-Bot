from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools
try:
	import argparse
	flags=argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags=none

def get_birthday(tmin,tmax):

    #REFERENCE :'https://developers.google.com/google-apps/calendar/v3/reference/events/list#try-it'
	SCOPES='https://www.googleapis.com/auth/calendar'
	CAL_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@import.calendar.google.com' 
    #calendar id of google calendar that imported from facebook calendar

	store=file.Storage('storage.json') 
	creds=store.get()

	if not creds or creds.invalid:
		flow=client.flow_from_clientsecrets('client_secret.json',SCOPES) #The file dowloaded from google developer console
		creds=tools.run_flow(flow,store,flags) \
			  if flags else tools.run(flow,store)

	CAL=build('calendar','v3',http=creds.authorize(Http())) 
	
	birth_list=[]
	page_token = None
	while True:

	  events = CAL.events().list(calendarId=CAL_ID, pageToken=page_token,timeMin=tmin+'T00:00:00+05:30',timeMax=tmax+'T23:59:59+05:30').execute()
	  
	  for event in events['items']:
		birth_list.append(event['summary'])
		
	  page_token = events.get('nextPageToken')

	  if not page_token:
		break

	return birth_list

def create_remainder(name,date):
    
    #REFERENCE:https://developers.google.com/google-apps/calendar/v3/reference/events/insert#examples
	SCOPES='https://www.googleapis.com/auth/calendar'

	store=file.Storage('storage.json')
	creds=store.get()

	if not creds or creds.invalid:
		flow=client.flow_from_clientsecrets('client_secret.json',SCOPES)
		creds=tools.run_flow(flow,store,flags) \
			  if flags else tools.run(flow,store)

	CAL=build('calendar','v3',http=creds.authorize(Http()))
	 
	#Events in JSON format
	EVENT={
	'summary':name,
	'start':{'dateTime':date+'T8:00:00+05:30'},
	'end':  {'dateTime':date+'T9:00:00+05:30'}
		  }

	response = CAL.events().insert(calendarId='primary',sendNotifications=True,body=EVENT).execute()
	
	if response['status']=='confirmed':
		return 'Success'
	else:
		return 'Error Occured'


def youtube_data(channel_name):
    
        #REFERENCE:https://developers.google.com/youtube/v3/docs/channels/list --For getting uploadid with channel name
        #REFERENCE:https://developers.google.com/youtube/v3/docs/playlistItems/list
	API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"#Google API key that obtained from the google developer console
	
	result=[]
	#uploads playlistID
	uploadID={'Computerpile':'UU9-y-6csu5WGm29I7JiwpnA','Vsauce':'UU6nSFpj9HTCZ5t-N3Rm3-HA','veritasium':'UUHnyfMqiRRG1u-2MsSQLbXA','Numberphile':'UUoxcjq-8xIDTYp3uz647V5A','TedX':'UUsT0YIqwnpJCM-mx7-gSA4Q'}

	SERVICE=build('youtube','v3',developerKey=API_KEY)

	if channel_name=='All':
		for name,ids in uploadID.items():
			response=SERVICE.playlistItems().list(part='snippet',maxResults=1,playlistId=ids).execute()
			result.append([response['items'][0]['snippet']['channelTitle'],response['items'][0]['snippet']['title'],response['items'][0]['snippet']['resourceId']['videoId']])
		
		return result

	if channel_name not in uploadID.keys():
		channel_name=channel_name.replace(' ','')
		print channel_name
		response=SERVICE.channels().list(part='contentDetails',forUsername=channel_name).execute()

		try:
		   playlistid1=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
		   uploadID[channel_name]=playlistid1
		except:
		   return 'Sorry Ajith, there is no youtube channel found named '

	try:
	
	   response=SERVICE.playlistItems().list(part='snippet',maxResults=1,playlistId=uploadID[channel_name]).execute()
	   #print type(response)
	   result.append([response['items'][0]['snippet']['channelTitle'],response['items'][0]['snippet']['title'],response['items'][0]['snippet']['resourceId']['videoId']])
	   return result
	except IndexError:
		return 'There is no videos in the uploads playlist of the channel '


