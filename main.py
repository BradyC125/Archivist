from __future__ import print_function
from apiclient import errors
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import json
import discord
import asyncio
import postSkimmer
from tokenHolder import *

SCOPES = ['https://www.googleapis.com/auth/script.projects',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents']

SCRIPT_ID = '1xct5low9IPZBtdUlVIk51PkK3Sy3n9q9FuVE21UBc_i5C67Fm6KFpdrc'

discordClient = discord.Client()

async def runBot():
  store = oauth_file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('script', 'v1', http=creds.authorize(Http()))
  
  await scrapeAndUpload(service)


async def scrapeAndUpload(service):
  print("Skim Pending")
  postList = await postSkimmer.skimPosts(discordClient)
  postList.sort(key= lambda message: message["dateTime"])
  for messageDict in postList:
    del messageDict["dateTime"]
  print("Skim Complete")
  request = {
    "function"   : "uploadMessages",
    "parameters" : json.dumps(postList),
    "devMode"    : True
  }
  
  try:
    print("Run Pending")
    response = service.scripts().run(body=request,scriptId=SCRIPT_ID).execute()
    print("Run Complete")
    
    if 'error' in response:
      error = response['error']['details'][0]
      print("Script error message: {0}".format(error['errorMessage']))

      if 'scriptStackTraceElements' in error:
        print("Script error stacktrace:")
        for trace in error['scriptStackTraceElements']:
          print("\t{0}: {1}".format(trace['function'],trace['lineNumber']))

  except errors.HttpError as e:
    print(e.content)

@discordClient.event
async def on_ready():
  print("Run Beginning")
  await runBot()

discordClient.run(botToken)
