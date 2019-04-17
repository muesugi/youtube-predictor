import os
import json
import config
import pymysql
import argparse
import sys

connection = pymysql.connect(host='127.0.0.1',
                            port = 3305,
                            user = config.USER,
                            password = config.PASSWORD,
                            db = 'video_data')

def create_tables():
    # Create tables (if they don't already exist)
    # TODO: create features table once we have all the features? or
    # create a table for each feature?
    # try:
    #     conn.execute(
    #         "CREATE TABLE IF NOT EXISTS features "
    #         + "(id VARCHAR(20) PRIMARY KEY, channelId TEXT, "
    #         + "playlistId TEXT, channelTitle TEXT, "
    #         + "title TEXT, description TEXT, duration TEXT, "
    #         + "categoryId INT, publishedAt TEXT, defaultAudioLanguage TEXT, "
    #         + "likeCount INT, dislikeCount INT, viewCount INT, commentCount INT);"
    #     )
    # except TypeError as e:
    #     print(e)
    #     return None
    pass


def query_videos(sqlquery, args=None, fetch_one=False):
    with connection.cursor() as cursor:
        if args:
            cursor.execute(sqlquery, args)
        else:
            cursor.execute(sqlquery)

        if fetch_one:
            return [cursor.fetchone()]
        else:
            return cursor.fetchall()

if __name__ == '__main__':
    print(query_videos("SELECT title FROM videos;"))
