import discord
import asyncio
import re

def getAttachments(message):
  attachmentList = []
  for att in message.attachments:
    attachmentList.append(att["proxy_url"])
  return attachmentList

def genReactionMessage(reactions):
  if reactions == []:
    return ''
  reactionString = "Reacted to by "
  for react in reactions:
    if react.custom_emoji:
      emojiToAdd = ":" + str(react.emoji).split(":")[1] + ":"
    else:
      emojiToAdd = react.emoji
    reactionString = reactionString + emojiToAdd + " (x" + str(react.count) + "), "
  return reactionString[:-2]

async def skimPosts(client):
  channel = client.get_channel('473993283060760576')
  messageArray = []
  async for message in client.logs_from(channel, limit=75000, reverse=True):
    if message.type == discord.MessageType.default:
      try:
        color = str(message.author.color)
      except:
        color = "#000000"
      messageArray.append({
        "dateTime"       : message.timestamp,
        "authorName"     : message.author.display_name,
        "authorColor"    : color,
        "messageContent" : message.clean_content,
        "attachments"    : getAttachments(message),
        "reactions"      : genReactionMessage(message.reactions)
      })
  return messageArray

