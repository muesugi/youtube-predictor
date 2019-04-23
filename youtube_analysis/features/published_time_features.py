from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt
import datetime

from youtube_analysis.videos_getter import query_videos

def published_dict():
    # Returns:
    #  Dictionary in the form videoid -> published time

    published_dict = {}
    published_results = query_videos("SELECT id, publishedAt FROM videos;")

    for r_tuple in published_results:
        vid, published = r_tuple
        published_time = parser.parse(published).time()
        if published_time < datetime.time(7,0,0):
            published_dict[vid] = "early morning"
        elif published_time > datetime.time(7,0,0) and published_time < datetime.time(12,0,0):
            published_dict[vid] = "late morning"
        elif published_time > datetime.time(12,0,0) and published_time < datetime.time(18,0,0):
            published_dict[vid] = "afternoon"
        elif published_time > datetime.time(18,0,0) and published_time < datetime.time(23,59,59):
            published_dict[vid] = "night"

    return published_dict

def feature_vector(video_ids):
    dict = published_dict()

    early_morn_vec = []
    late_morn_vec = []
    afternoon_vec = []
    night_vec = []

    for id in video_ids:
        time = dict[id]
        if time == "early morning":
            early_morn_vec.append(1)
            late_morn_vec.append(0)
            afternoon_vec.append(0)
            night_vec.append(0)
        if time == "late morning":
            early_morn_vec.append(0)
            late_morn_vec.append(1)
            afternoon_vec.append(0)
            night_vec.append(0)
        if time == "afternoon":
            early_morn_vec.append(0)
            late_morn_vec.append(0)
            afternoon_vec.append(1)
            night_vec.append(0)
        if time == "night":
            early_morn_vec.append(0)
            late_morn_vec.append(0)
            afternoon_vec.append(0)
            night_vec.append(1)

    return [early_morn_vec, late_morn_vec, afternoon_vec, night_vec]

def published_plot_all():
    # No params or return
    # Plots all durations vs viewCount

    published_results = query_videos("SELECT id, publishedAt FROM videos WHERE viewCount IS NOT NULL;")

    published_count = {"early morning": 0, "late morning": 0, "afternoon": 0, "night": 0}

    for r_tuple in published_results:
        id, publishedAt = r_tuple
        published_time = parser.parse(publishedAt).time()
        if published_time < datetime.time(7,0,0):
            published_count["early morning"] += 1
        elif published_time > datetime.time(7,0,0) and published_time < datetime.time(12,0,0):
            published_count["late morning"] += 1
        elif published_time > datetime.time(12,0,0) and published_time < datetime.time(18,0,0):
            published_count["afternoon"] += 1
        elif published_time > datetime.time(18,0,0) and published_time < datetime.time(23,59,59):
            published_count["night"] += 1

    X = list(published_count.keys())
    y = list(published_count.values())

    plt.bar(np.arange(len(X)), np.array(y), align='center', alpha=0.5)
    plt.xticks(np.arange(len(X)), np.array(X))
    plt.xlabel('time of day')
    plt.ylabel('number of videos published')
    plt.show()

def duration_plot_averages():
    # No params or return
    # Plots durations vs average viewCount for that duration,
    # and then uses polyfit to draw a polynomial line representing this curve

    published_results = query_videos("SELECT id, publishedAt, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    published_views = {"early morning": [], "late morning": [], "afternoon": [], "night": []}

    for r_tuple in published_results:
        id, publishedAt, viewCount = r_tuple
        published_time = parser.parse(publishedAt).time()
        if published_time < datetime.time(7,0,0):
            published_views["early morning"].append(viewCount)
        elif published_time > datetime.time(7,0,0) and published_time < datetime.time(12,0,0):
            published_views["late morning"].append(viewCount)
        elif published_time > datetime.time(12,0,0) and published_time < datetime.time(18,0,0):
            published_views["afternoon"].append(viewCount)
        elif published_time > datetime.time(18,0,0) and published_time < datetime.time(23,59,59):
            published_views["night"].append(viewCount)

    published_to_viewavg = {published: sum(viewlist)/len(viewlist) for published, viewlist in published_views.items()}

    x_avg = list(published_views.keys())
    y_avg = [published_to_viewavg[published] for published in x_avg]

    plt.bar(np.arange(len(x_avg)), np.array(y_avg), align='center', alpha=0.5)
    plt.xticks(np.arange(len(x_avg)), np.array(x_avg))

    plt.xlabel('published time')
    plt.ylabel('average view counts')

    plt.show()

if __name__ == '__main__':
    published_dict()
    published_plot_all()
    duration_plot_averages()
