from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt
import datetime

from youtube_analysis.videos_getter import query_videos

def published_dict():
    # Returns:
    #  Dictionary in the form published time -> video count

    published_dict = {}
    published_results = query_videos("SELECT id, publishedAt FROM videos;")

    for r_tuple in published_results:
        vid, published = r_tuple
        published_time = parser.parse(published).time()
        if published_time < datetime.time(1,0,0):
            if "12 am" in published_dict:
                published_dict["12 am"] += 1
            else:
                published_dict["12 am"] = 1
        elif published_time < datetime.time(2,0,0):
            if "1 am" in published_dict:
                published_dict["1 am"] += 1
            else:
                published_dict["1 am"] = 1
        elif published_time < datetime.time(3,0,0):
            if "2 am" in published_dict:
                published_dict["2 am"] += 1
            else:
                published_dict["2 am"] = 1
        elif published_time < datetime.time(4,0,0):
            if "3 am" in published_dict:
                published_dict["3 am"] += 1
            else:
                published_dict["3 am"] = 1
        elif published_time < datetime.time(5,0,0):
            if "4 am" in published_dict:
                published_dict["4 am"] += 1
            else:
                published_dict["4 am"] = 1
        elif published_time < datetime.time(6,0,0):
            if "5 am" in published_dict:
                published_dict["5 am"] += 1
            else:
                published_dict["5 am"] = 1
        elif published_time < datetime.time(7,0,0):
            if "6 am" in published_dict:
                published_dict["6 am"] += 1
            else:
                published_dict["6 am"] = 1
        elif published_time < datetime.time(8,0,0):
            if "7 am" in published_dict:
                published_dict["7 am"] += 1
            else:
                published_dict["7 am"] = 1
        elif published_time < datetime.time(9,0,0):
            if "8 am" in published_dict:
                published_dict["8 am"] += 1
            else:
                published_dict["8 am"] = 1
        elif published_time < datetime.time(10,0,0):
            if "9 am" in published_dict:
                published_dict["9 am"] += 1
            else:
                published_dict["9 am"] = 1
        elif published_time < datetime.time(11,0,0):
            if "10 am" in published_dict:
                published_dict["10 am"] += 1
            else:
                published_dict["10 am"] = 1
        elif published_time < datetime.time(12,0,0):
            if "11 am" in published_dict:
                published_dict["11 am"] += 1
            else:
                published_dict["11 am"] = 1
        elif published_time < datetime.time(13,0,0):
            if "12 pm" in published_dict:
                published_dict["12 pm"] += 1
            else:
                published_dict["12 pm"] = 1
        elif published_time < datetime.time(14,0,0):
            if "1 pm" in published_dict:
                published_dict["1 pm"] += 1
            else:
                published_dict["1 pm"] = 1
        elif published_time < datetime.time(15,0,0):
            if "2 pm" in published_dict:
                published_dict["2 pm"] += 1
            else:
                published_dict["2 pm"] = 1
        elif published_time < datetime.time(16,0,0):
            if "3 pm" in published_dict:
                published_dict["3 pm"] += 1
            else:
                published_dict["3 pm"] = 1
        elif published_time < datetime.time(17,0,0):
            if "4 pm" in published_dict:
                published_dict["4 pm"] += 1
            else:
                published_dict["4 pm"] = 1
        elif published_time < datetime.time(18,0,0):
            if "5 pm" in published_dict:
                published_dict["5 pm"] += 1
            else:
                published_dict["5 pm"] = 1
        elif published_time < datetime.time(19,0,0):
            if "6 pm" in published_dict:
                published_dict["6 pm"] += 1
            else:
                published_dict["6 pm"] = 1
        elif published_time < datetime.time(20,0,0):
            if "7 pm" in published_dict:
                published_dict["7 pm"] += 1
            else:
                published_dict["7 pm"] = 1
        elif published_time < datetime.time(21,0,0):
            if "8 pm" in published_dict:
                published_dict["8 pm"] += 1
            else:
                published_dict["8 pm"] = 1
        elif published_time < datetime.time(22,0,0):
            if "9 pm" in published_dict:
                published_dict["9 pm"] += 1
            else:
                published_dict["9 pm"] = 1
        elif published_time < datetime.time(23,0,0):
            if "10 pm" in published_dict:
                published_dict["10 pm"] += 1
            else:
                published_dict["10 pm"] = 1
        elif published_time <= datetime.time(23,59,59):
            if "11 pm - 11" in published_dict:
                published_dict["11 pm"] += 1
            else:
                published_dict["11 pm"] = 1

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

    published_count = published_dict()

    X = list(published_count.keys())
    y = list(published_count.values())

    plt.bar(np.arange(len(X)), np.array(y), align='center', alpha=0.5)
    plt.xticks(np.arange(len(X)), np.array(X), rotation='vertical')
    plt.xlabel('time of day')
    plt.ylabel('number of videos published')
    plt.show()

def duration_plot_averages():
    # No params or return
    # Plots durations vs average viewCount for that duration,
    # and then uses polyfit to draw a polynomial line representing this curve

    published_results = query_videos("SELECT id, publishedAt, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    published_dict = {}

    for r_tuple in published_results:
        id, publishedAt, viewCount = r_tuple
        published_time = parser.parse(publishedAt).time()
        if published_time < datetime.time(1,0,0):
            if "12 am" in published_dict:
                published_dict["12 am"].append(viewCount)
            else:
                published_dict["12 am"] = [viewCount]
        elif published_time < datetime.time(2,0,0):
            if "1 am" in published_dict:
                published_dict["1 am"].append(viewCount)
            else:
                published_dict["1 am"] = [viewCount]
        elif published_time < datetime.time(3,0,0):
            if "2 am" in published_dict:
                published_dict["2 am"].append(viewCount)
            else:
                published_dict["2 am"] = [viewCount]
        elif published_time < datetime.time(4,0,0):
            if "3 am" in published_dict:
                published_dict["3 am"].append(viewCount)
            else:
                published_dict["3 am"] = [viewCount]
        elif published_time < datetime.time(5,0,0):
            if "4 am" in published_dict:
                published_dict["4 am"].append(viewCount)
            else:
                published_dict["4 am"] = [viewCount]
        elif published_time < datetime.time(6,0,0):
            if "5 am" in published_dict:
                published_dict["5 am"].append(viewCount)
            else:
                published_dict["5 am"] = [viewCount]
        elif published_time < datetime.time(7,0,0):
            if "6 am" in published_dict:
                published_dict["6 am"].append(viewCount)
            else:
                published_dict["6 am"] = [viewCount]
        elif published_time < datetime.time(8,0,0):
            if "7 am" in published_dict:
                published_dict["7 am"].append(viewCount)
            else:
                published_dict["7 am"] = [viewCount]
        elif published_time < datetime.time(9,0,0):
            if "8 am" in published_dict:
                published_dict["8 am"].append(viewCount)
            else:
                published_dict["8 am"] = [viewCount]
        elif published_time < datetime.time(10,0,0):
            if "9 am" in published_dict:
                published_dict["9 am"].append(viewCount)
            else:
                published_dict["9 am"] = [viewCount]
        elif published_time < datetime.time(11,0,0):
            if "10 am" in published_dict:
                published_dict["10 am"].append(viewCount)
            else:
                published_dict["10 am"] = [viewCount]
        elif published_time < datetime.time(12,0,0):
            if "11 am" in published_dict:
                published_dict["11 am"].append(viewCount)
            else:
                published_dict["11 am"] = [viewCount]
        elif published_time < datetime.time(13,0,0):
            if "12 pm" in published_dict:
                published_dict["12 pm"].append(viewCount)
            else:
                published_dict["12 pm"] = [viewCount]
        elif published_time < datetime.time(14,0,0):
            if "1 pm" in published_dict:
                published_dict["1 pm"].append(viewCount)
            else:
                published_dict["1 pm"] = [viewCount]
        elif published_time < datetime.time(15,0,0):
            if "2 pm" in published_dict:
                published_dict["2 pm"].append(viewCount)
            else:
                published_dict["2 pm"] = [viewCount]
        elif published_time < datetime.time(16,0,0):
            if "3 pm" in published_dict:
                published_dict["3 pm"].append(viewCount)
            else:
                published_dict["3 pm"] = [viewCount]
        elif published_time < datetime.time(17,0,0):
            if "4 pm" in published_dict:
                published_dict["4 pm"].append(viewCount)
            else:
                published_dict["4 pm"] = [viewCount]
        elif published_time < datetime.time(18,0,0):
            if "5 pm" in published_dict:
                published_dict["5 pm"].append(viewCount)
            else:
                published_dict["5 pm"] = [viewCount]
        elif published_time < datetime.time(19,0,0):
            if "6 pm" in published_dict:
                published_dict["6 pm"].append(viewCount)
            else:
                published_dict["6 pm"] = [viewCount]
        elif published_time < datetime.time(20,0,0):
            if "7 pm" in published_dict:
                published_dict["7 pm"].append(viewCount)
            else:
                published_dict["7 pm"] = [viewCount]
        elif published_time < datetime.time(21,0,0):
            if "8 pm" in published_dict:
                published_dict["8 pm"].append(viewCount)
            else:
                published_dict["8 pm"] = [viewCount]
        elif published_time < datetime.time(22,0,0):
            if "9 pm" in published_dict:
                published_dict["9 pm"].append(viewCount)
            else:
                published_dict["9 pm"] = [viewCount]
        elif published_time < datetime.time(23,0,0):
            if "10 pm" in published_dict:
                published_dict["10 pm"].append(viewCount)
            else:
                published_dict["10 pm"] = [viewCount]
        elif published_time <= datetime.time(23,59,59):
            if "11 pm - 11" in published_dict:
                published_dict["11 pm"].append(viewCount)
            else:
                published_dict["11 pm"] = [viewCount]

    published_to_viewavg = {published: sum(viewlist)/len(viewlist) for published, viewlist in published_dict.items()}

    x_avg = list(published_dict.keys())
    y_avg = [published_to_viewavg[published] for published in x_avg]

    plt.bar(np.arange(len(x_avg)), np.array(y_avg), align='center', alpha=0.5)
    plt.xticks(np.arange(len(x_avg)), np.array(x_avg), rotation='vertical')

    plt.xlabel('published time')
    plt.ylabel('average view counts')

    plt.show()

if __name__ == '__main__':
    # published_dict()
    # published_plot_all()
    duration_plot_averages()
