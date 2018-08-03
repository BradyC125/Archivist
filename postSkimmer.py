import discord
import asyncio
import re

def getAttachments(message, drive_service):
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

async def skimPosts(client, drive_service):
  channel = client.get_channel('205167432652947456')
  messageArray = []
  async for message in client.logs_from(channel, limit=1000, reverse=True):
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
        "attachments"    : getAttachments(message, drive_service),
        "reactions"      : genReactionMessage(message.reactions)
      })
  return messageArray

