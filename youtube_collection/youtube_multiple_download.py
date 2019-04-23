import os
import json
import config
import pymysql
import argparse
import sys

import google.oauth2.credentials

# REMEMBER TO INSTALL NECESSARY PACKAGES when running for the first time!
# 1. pip install --upgrade google-api-python-client
# 2. pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
KEY = config.KEY
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

connection = pymysql.connect(host='127.0.0.1',
                            port = 3305,
                            user = config.USER,
                            password = config.PASSWORD,
                            db = 'video_data')
conn = connection.cursor()

def create_tables():
    # Create tables (if they don't already exist)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS videos "
            + "(id VARCHAR(20) PRIMARY KEY, channelId TEXT, "
            + "playlistId TEXT, channelTitle TEXT, "
            + "title TEXT, description TEXT, duration TEXT, "
            + "categoryId INT, publishedAt TEXT, defaultAudioLanguage TEXT, "
            + "likeCount INT, dislikeCount INT, viewCount INT, commentCount INT);"
        )
    except TypeError as e:
        print(e)
        return None


def get_authenticated_service():
    # structure from https://medium.com/greyatom/youtube-data-in-python-6147160c5833,
    return build(API_SERVICE_NAME, API_VERSION, developerKey=KEY )

def related_playlists_by_channel_id(client, **kwargs):
    # docs: https://developers.google.com/youtube/v3/docs/channels/list
    response = client.channels().list(
        **kwargs
    ).execute()

    #TODO: handle error: non existence of channel id
    return response["items"][0]["contentDetails"]["relatedPlaylists"]

def playlist_items_list_by_playlist_id(client, **kwargs):
    # docs: https://developers.google.com/youtube/v3/docs/playlistItems/list
    response = client.playlistItems().list(
        **kwargs
    ).execute()

    return response

# DEPRECATED
def all_videos_by_playlist_id(client, playlist_id):
    # pagination
    videos = []

    playlist_list_response = playlist_items_list_by_playlist_id(client,
        part='snippet,contentDetails',
            maxResults=50, # max accepted is 50; defaults to 5
            playlistId=playlist_id,
    )
    videos += playlist_list_response["items"]
    print("Total # results should be:", playlist_list_response["pageInfo"]["totalResults"])


    # youtube data api uses pagination;
    # keep going until no more videos
    # TODO: check if there's a limit to pages
    while 'nextPageToken' in playlist_list_response:
        playlist_list_response = playlist_items_list_by_playlist_id(client,
            part='snippet,contentDetails',
            maxResults=50, # max accepted is 50; defaults to 5
            pageToken=playlist_list_response['nextPageToken'],
            playlistId=playlist_id,
        )
        videos += playlist_list_response["items"]

    return videos

def all_video_data_by_playlist_id(client, playlist_id):
    # Calls both playlist list endpoint and videos list endpoint
    # pagination
    videos = []

    is_first_call = True
    next_page_token = None

    while is_first_call or next_page_token:
        kwargs = dict(
            part='contentDetails', # need content details for the video id, which is not playlistitemid
            maxResults=50, # max accepted is 50; defaults to 5
            playlistId=playlist_id,
        )

        if next_page_token:
            kwargs['pageToken'] = next_page_token

        ids_response = playlist_items_list_by_playlist_id(client, **kwargs)

        if is_first_call:
            print("Total # results should be:", ids_response["pageInfo"]["totalResults"])
            is_first_call = False

        ids_str = ",".join([vid["contentDetails"]["videoId"] for vid in ids_response["items"]])

        # have to do a separate call to videos list endpoint to get statistics.
        # included in this one since the call takes a max of 50 ids concatenated in 'id' param
        video_content_response = videos_list_by_id(client,
            part='contentDetails,snippet,statistics', # content details is redundant here, TODO: restore data from call 1
            id=ids_str,
        )
        videos.extend(video_content_response["items"])

        next_page_token = ids_response['nextPageToken'] if 'nextPageToken' in ids_response else None

    return videos

def videos_list_by_id(client, **kwargs):
    response = client.videos().list(
        **kwargs
    ).execute()

    return response

def channel_id_by_user_id(client, **kwargs):
    response = client.channels().list(
        **kwargs
    ).execute()

    return response['items'][0]['id']

###### Higher level functions ###
def write_to_json(file_identifier, videos):
    file_name =  'videos_{}.json'.format(file_identifier)

    with open(file_name, 'w+') as output_file:
        json.dump(videos, output_file)
        print("{} results written to {}".format(len(videos), file_name))

def run_upload(cuid, is_user_id=False):
    ### GET CHANNEL ID of channel in question ###
    # assume the cuid is a channel id unless told otherwise
    channel_id = cuid
    # if user id has been specified, find the channel id from the user id
    if is_user_id:
        channel_id = channel_id_by_user_id(client,
        part='id',
        forUsername=channel_id)
        print("user id:", cuid, "channel id:", channel_id)
    else:
        print("channel_id: ", channel_id)

    ### 2. GET PLAYLIST ID OF ALL UPLOADS FROM THE CHANNEL ID ###
    related_playlists = related_playlists_by_channel_id( client,
                            part='contentDetails',
                            id=channel_id )
    uploaded_playlist_id = related_playlists["uploads"]
    print("uploaded_playlist_id: ", uploaded_playlist_id)

    ### 3. GET VIDEO INFO FROM PLAYLIST ID & OUTPUT TO FILE ###
    # NOTE: this is just proof of concept, this is would be where we upload to a database.
    videos = all_video_data_by_playlist_id(client, uploaded_playlist_id)

    create_tables()

    for video in videos:
        id = video['id']
        channelId = video['snippet']['channelId']
        channelTitle = video['snippet']['channelTitle']
        videoTitle = video['snippet']['title']
        desc = video['snippet']['description']
        duration = video['contentDetails']['duration']
        categoryId = video['snippet']['categoryId']
        publishedAt = video['snippet']['publishedAt']

        # columns that may not exist in the data. .get returns None if dne
        likeCount = video['statistics'].get('likeCount')
        dislikeCount = video['statistics'].get('dislikeCount')
        viewCount = video['statistics'].get('viewCount')
        defaultLang = video['snippet'].get('defaultAudioLanguage')
        # tags = video['snippet'].get('tags')
        commentCount = video['statistics'].get('commentCount')

        # add video details to db here
        try:
            sql = "INSERT IGNORE INTO videos(id, channelId, playlistId, channelTitle, title, description, duration, categoryId, publishedAt, defaultAudioLanguage, likeCount, dislikeCount, viewCount, commentCount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            vals = (id, channelId, uploaded_playlist_id, channelTitle, videoTitle, desc, duration,
            categoryId, publishedAt, defaultLang, likeCount, dislikeCount, viewCount,
            commentCount)
            conn.execute(sql, vals)
            connection.commit()
        except TypeError as e:
            print(e)

    conn.close()

    # write_to_json(cuid if is_user_id else channel_id, videos)


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()

    #----- Command Line Args --------#
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--userids", dest="user_ids", help="One or more User ID of channel user", nargs='+')
    parser.add_argument("-c", "--channelids", dest="channel_ids", help="One or more Channel ID of channel", nargs='+')

    args = parser.parse_args()

    # make sure at leaset one parameter is set
    if bool(args.user_ids) + bool(args.channel_ids) == 0:
        print("Error: must specify at least one user id or channel id. `python3 -c <channel-id> is probably what you want.`")
        sys.exit()

    for cid in args.channel_ids:
        run_upload(cid)

    for uid in args.user_ids:
        run_upload(uid, is_user_id=True)

    # / ----- Command Line Args --------#
