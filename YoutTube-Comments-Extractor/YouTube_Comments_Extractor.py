#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:17:03 2019

@author: jdavidmartinezg
"""

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

#                         SETUP - RUN EVERY TIME

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************


import os
import pandas as pd
import google.oauth2.credentials
import numpy as np
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import time
import requests
import json
import matplotlib.pyplot as plt
import os
import datetime as dt
import seaborn as sns
import collections
from functools import reduce


# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************




#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#                       YouTube API connection

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------






# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.



developer_key = "<YOUR CLIENT SECRET HERE>"
# alternative developer key
# developer_key = "AIzaSyCmb020Ke_LIRvnewigKY-IFKEE4yIaY-E"



# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def channels_list_by_username(service, **kwargs):
  results = service.channels().list(
    **kwargs
  ).execute()

  print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
       (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount']))

#if __name__ == '__main__':
#  # When running locally, disable OAuthlib's HTTPs verification. When
#  # running in production *do not* leave this option enabled.
#  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#  service = get_authenticated_service()
#  channels_list_by_username(service,
#      part='snippet,contentDetails,statistics',
#      forUsername='GoogleDevelopers')


# Text analysis and network analysis


def load_comments(match):

    total_comments_data = {"video_id":[],
                           "comment_id":[],
                           "reply_count":[],
                           "author":[],
                           "author_channel_id":[],
                           "likes_count":[],
                           "time":[],
                           "text":[]}

    for item in match["items"]:
        comment           = item["snippet"]["topLevelComment"]
        comment_id        = item['id']
        reply_count       = item["snippet"]["totalReplyCount"]
        video_id          = item["snippet"]["videoId"]
        author            = comment["snippet"]["authorDisplayName"]
        author_channel_id = comment["snippet"]["authorChannelId"]["value"]
        likes             = comment["snippet"]["likeCount"]
        time              = comment["snippet"]["publishedAt"]
        text              = comment["snippet"]["textDisplay"]

        comment_data = {"video_id":[video_id],
                        "comment_id":[comment_id],
                        "reply_count":[reply_count],
                        "author":[author],
                        "author_channel_id":[author_channel_id],
                        "likes_count":[likes],
                        "time":[time],
                        "text":[text]}

        total_comments_data["video_id"]          = total_comments_data["video_id"] + comment_data["video_id"]
        total_comments_data["comment_id"]        = total_comments_data["comment_id"] + comment_data["comment_id"]
        total_comments_data["reply_count"]       = total_comments_data["reply_count"] + comment_data["reply_count"]
        total_comments_data["author"]            = total_comments_data["author"] + comment_data["author"]
        total_comments_data["author_channel_id"] = total_comments_data["author_channel_id"] + comment_data["author_channel_id"]
        total_comments_data["likes_count"]       = total_comments_data["likes_count"] + comment_data["likes_count"]
        total_comments_data["time"]              = total_comments_data["time"] + comment_data["time"]
        total_comments_data["text"]              = total_comments_data["text"] + comment_data["text"]

    return total_comments_data


def load_videos(match):

    total_videos_data = {"video_id":[],
                         "description":[],
                         "liveBroadcastContent":[],
                         "publishedAt":[],
                         "title":[],
                         "channelTitle":[]}

    for item in match["items"]:
        try:
            video_id         = item["id"]["videoId"]
        except:
            video_id         = "Not a video"
        description          = item["snippet"]["description"]
        liveBroadcastContent = item["snippet"]["liveBroadcastContent"]
        publishedAt          = item["snippet"]["publishedAt"]
        title                = item["snippet"]["title"]
        channelTitle         = item["snippet"]["channelTitle"]

        video_data = {"video_id":[video_id],
                      "description":[description],
                      "liveBroadcastContent":[liveBroadcastContent],
                      "publishedAt":[publishedAt],
                      "title":[title],
                      "channelTitle":[channelTitle]}

        total_videos_data["video_id"]             = total_videos_data["video_id"] + video_data["video_id"]
        total_videos_data["description"]          = total_videos_data["description"] + video_data["description"]
        total_videos_data["liveBroadcastContent"] = total_videos_data["liveBroadcastContent"] + video_data["liveBroadcastContent"]
        total_videos_data["publishedAt"]          = total_videos_data["publishedAt"] + video_data["publishedAt"]
        total_videos_data["title"]                = total_videos_data["title"] + video_data["title"]
        total_videos_data["channelTitle"]         = total_videos_data["channelTitle"] + video_data["channelTitle"]

    return total_videos_data



#
#def load_replies(match):
#
#    total_replies_data = {"video_id":[],
#                           "reply_count":[],
#                           "author":[],
#                           "author_channel_id":[],
#                           "likes_count":[],
#                           "time":[],
#                           "text":[]}
#
#    for item in match["items"]:
#
#        video_id = item["snippet"]["videoId"]
#        comment_id = item['id']
#
#        if 'replies' in item.keys():
#            for reply in item['replies']['comments']:
#                rauthor = reply['snippet']['authorDisplayName']
#                rtext = reply["snippet"]["textDisplay"]
#
##       REPLIES
##        #
##        if 'replies' in item.keys():
##            for reply in item['replies']['comments']:
##                rauthor = reply['snippet']['authorDisplayName']
##                rtext = reply["snippet"]["textDisplay"]
##            print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")



##### BETTER METHOD WITHOUT AUTHENTICATION


########################## Extract all videos IDS

channel_id = "<THE DESIRED CHANNEL'S ID>"

r = requests.get("https://www.googleapis.com/youtube/v3/search?key="+ developer_key +"&channelId=" + channel_id + "&part=snippet,id&order=date&maxResults=50")
list_of_videos_1st_dict = r.json()
videos_whole_dict = load_videos(list_of_videos_1st_dict)
nextPageToken = list_of_videos_1st_dict.get("nextPageToken")


# Retrieve all the rest of the videos
while nextPageToken:
    r = requests.get("https://www.googleapis.com/youtube/v3/search?key="+ developer_key +"&channelId=" + channel_id + "&part=snippet,id&order=date&maxResults=50&pageToken=" + nextPageToken)
    videos_further_dict_o = r.json()
    videos_further_dict = load_videos(videos_further_dict_o)

    videos_whole_dict["video_id"]             = videos_whole_dict["video_id"] + videos_further_dict["video_id"]
    videos_whole_dict["description"]          = videos_whole_dict["description"] + videos_further_dict["description"]
    videos_whole_dict["liveBroadcastContent"] = videos_whole_dict["liveBroadcastContent"] + videos_further_dict["liveBroadcastContent"]
    videos_whole_dict["publishedAt"]          = videos_whole_dict["publishedAt"] + videos_further_dict["publishedAt"]
    videos_whole_dict["title"]                = videos_whole_dict["title"] + videos_further_dict["title"]
    videos_whole_dict["channelTitle"]         = videos_whole_dict["channelTitle"] + videos_further_dict["channelTitle"]


    print(len(videos_whole_dict["title"]))

    nextPageToken = videos_further_dict_o.get("nextPageToken")

    print(nextPageToken)

videos_dataset = pd.DataFrame(videos_whole_dict)

videos_dataset = videos_dataset.drop_duplicates()


########################## MOTHERSHIP DATABASE OF COMMENTS

mothership_comments = pd.DataFrame(columns = ['author',
                                              'comment_id',
                                              'author_channel_id',
                                              'likes_count',
                                              'reply_count',
                                              'text',
                                              'time',
                                              'video_id'])

ids = list(videos_dataset[videos_dataset["video_id"] != "Not a video"]['video_id'])

for video_id in ids:

    print("Video -> " + str(video_id))

    try:

        r = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+ developer_key +"&part=snippet&videoId="+ video_id +"&maxResults=100")
        comments_1st_dict = r.json()
        comments_whole_dict = load_comments(comments_1st_dict)
        nextPageToken = comments_1st_dict.get("nextPageToken")

        # Retrieve all the rest of the pages
        while nextPageToken:
            r = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+ developer_key +"&part=snippet&videoId="+ video_id +"&maxResults=100&pageToken=" + nextPageToken)
            comments_further_dict_o = r.json()
            comments_further_dict = load_comments(comments_further_dict_o)

            comments_whole_dict["video_id"]          = comments_whole_dict["video_id"] + comments_further_dict["video_id"]
            comments_whole_dict["reply_count"]       = comments_whole_dict["reply_count"] + comments_further_dict["reply_count"]
            comments_whole_dict["author"]            = comments_whole_dict["author"] + comments_further_dict["author"]
            comments_whole_dict["author_channel_id"] = comments_whole_dict["author_channel_id"] + comments_further_dict["author_channel_id"]
            comments_whole_dict["likes_count"]       = comments_whole_dict["likes_count"] + comments_further_dict["likes_count"]
            comments_whole_dict["time"]              = comments_whole_dict["time"] + comments_further_dict["time"]
            comments_whole_dict["text"]              = comments_whole_dict["text"] + comments_further_dict["text"]
            comments_whole_dict["comment_id"]        = comments_whole_dict["comment_id"] + comments_further_dict["comment_id"]

            #print(len(comments_whole_dict["text"]))

            nextPageToken = comments_further_dict_o.get("nextPageToken")

            #print(nextPageToken)

        dataset = pd.DataFrame(comments_whole_dict)

        dataset = dataset.drop_duplicates()

        mothership_comments = pd.concat([mothership_comments, dataset])

        print("GENERAL SIZE OF comments database ->" + str(len(mothership_comments)))

        time.sleep(5)


    except:

        print(video_id + " API limit reached...Resuming retireval in 5 minutes...")

        time.sleep(300)

        r = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+ developer_key +"&part=snippet&videoId="+ video_id +"&maxResults=100")
        comments_1st_dict = r.json()
        comments_whole_dict = load_comments(comments_1st_dict)
        nextPageToken = comments_1st_dict.get("nextPageToken")

        # Retrieve all the rest of the pages
        while nextPageToken:
            r = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+ developer_key +"&part=snippet&videoId="+ video_id +"&maxResults=100&pageToken=" + nextPageToken)
            comments_further_dict_o = r.json()
            comments_further_dict = load_comments(comments_further_dict_o)

            comments_whole_dict["video_id"]          = comments_whole_dict["video_id"] + comments_further_dict["video_id"]
            comments_whole_dict["reply_count"]       = comments_whole_dict["reply_count"] + comments_further_dict["reply_count"]
            comments_whole_dict["author"]            = comments_whole_dict["author"] + comments_further_dict["author"]
            comments_whole_dict["author_channel_id"] = comments_whole_dict["author_channel_id"] + comments_further_dict["author_channel_id"]
            comments_whole_dict["likes_count"]       = comments_whole_dict["likes_count"] + comments_further_dict["likes_count"]
            comments_whole_dict["time"]              = comments_whole_dict["time"] + comments_further_dict["time"]
            comments_whole_dict["text"]              = comments_whole_dict["text"] + comments_further_dict["text"]
            comments_whole_dict["comment_id"]        = comments_whole_dict["comment_id"] + comments_further_dict["comment_id"]

            #print(len(comments_whole_dict["text"]))

            nextPageToken = comments_further_dict_o.get("nextPageToken")

            #print(nextPageToken)

        dataset = pd.DataFrame(comments_whole_dict)

        dataset = dataset.drop_duplicates()

        mothership_comments = pd.concat([mothership_comments, dataset])

        print("GENERAL SIZE OF comments database -> " + str(len(mothership_comments)))

        time.sleep(5)


## Merge Video_id info

mothership_comments = pd.merge(mothership_comments, videos_dataset, on = "video_id", how = "left")

len(list(mothership_comments))

mothership_comments.columns = ['comment_author',
 'comment_author_channel_id',
 'comment_id',
 'comment_likes_count',
 'comment_reply_count',
 'comment_text',
 'comment_datepoint',
 'video_id',
 'video_channelTitle',
 'video_description',
 'video_liveBroadcastContent',
 'video_publishedAt',
 'video_title']

## Replies retrieval
