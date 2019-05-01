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
            if "00:00-00:59" in published_dict:
                published_dict["00:00-00:59"] += 1
            else:
                published_dict["00:00-00:59"] = 1
        elif published_time < datetime.time(2,0,0):
            if "01:00-01:59" in published_dict:
                published_dict["01:00-01:59"] += 1
            else:
                published_dict["01:00-01:59"] = 1
        elif published_time < datetime.time(3,0,0):
            if "02:00-02:59" in published_dict:
                published_dict["02:00-02:59"] += 1
            else:
                published_dict["02:00-02:59"] = 1
        elif published_time < datetime.time(4,0,0):
            if "03:00-03:59" in published_dict:
                published_dict["03:00-03:59"] += 1
            else:
                published_dict["03:00-03:59"] = 1
        elif published_time < datetime.time(5,0,0):
            if "04:00-04:59" in published_dict:
                published_dict["04:00-04:59"] += 1
            else:
                published_dict["04:00-04:59"] = 1
        elif published_time < datetime.time(6,0,0):
            if "05:00-05:59" in published_dict:
                published_dict["05:00-05:59"] += 1
            else:
                published_dict["05:00-05:59"] = 1
        elif published_time < datetime.time(7,0,0):
            if "06:00-06:59" in published_dict:
                published_dict["06:00-06:59"] += 1
            else:
                published_dict["06:00-06:59"] = 1
        elif published_time < datetime.time(8,0,0):
            if "07:00-07:59" in published_dict:
                published_dict["07:00-07:59"] += 1
            else:
                published_dict["07:00-07:59"] = 1
        elif published_time < datetime.time(9,0,0):
            if "08:00-08:59" in published_dict:
                published_dict["08:00-08:59"] += 1
            else:
                published_dict["08:00-08:59"] = 1
        elif published_time < datetime.time(10,0,0):
            if "09:00-09:59" in published_dict:
                published_dict["09:00-09:59"] += 1
            else:
                published_dict["09:00-09:59"] = 1
        elif published_time < datetime.time(11,0,0):
            if "10:00-10:59" in published_dict:
                published_dict["10:00-10:59"] += 1
            else:
                published_dict["10:00-10:59"] = 1
        elif published_time < datetime.time(12,0,0):
            if "11:00-11:59" in published_dict:
                published_dict["11:00-11:59"] += 1
            else:
                published_dict["11:00-11:59"] = 1
        elif published_time < datetime.time(13,0,0):
            if "12:00-12:59" in published_dict:
                published_dict["12:00-12:59"] += 1
            else:
                published_dict["12:00-12:59"] = 1
        elif published_time < datetime.time(14,0,0):
            if "13:00-13:59" in published_dict:
                published_dict["13:00-13:59"] += 1
            else:
                published_dict["13:00-13:59"] = 1
        elif published_time < datetime.time(15,0,0):
            if "14:00-14:59" in published_dict:
                published_dict["14:00-14:59"] += 1
            else:
                published_dict["14:00-14:59"] = 1
        elif published_time < datetime.time(16,0,0):
            if "15:00-15:59" in published_dict:
                published_dict["15:00-15:59"] += 1
            else:
                published_dict["15:00-15:59"] = 1
        elif published_time < datetime.time(17,0,0):
            if "16:00-16:59" in published_dict:
                published_dict["16:00-16:59"] += 1
            else:
                published_dict["16:00-16:59"] = 1
        elif published_time < datetime.time(18,0,0):
            if "17:00-17:59" in published_dict:
                published_dict["17:00-17:59"] += 1
            else:
                published_dict["17:00-17:59"] = 1
        elif published_time < datetime.time(19,0,0):
            if "18:00-18:59" in published_dict:
                published_dict["18:00-18:59"] += 1
            else:
                published_dict["18:00-18:59"] = 1
        elif published_time < datetime.time(20,0,0):
            if "19:00-19:59" in published_dict:
                published_dict["19:00-19:59"] += 1
            else:
                published_dict["19:00-19:59"] = 1
        elif published_time < datetime.time(21,0,0):
            if "20:00-20:59" in published_dict:
                published_dict["20:00-20:59"] += 1
            else:
                published_dict["20:00-20:59"] = 1
        elif published_time < datetime.time(22,0,0):
            if "21:00-21:59" in published_dict:
                published_dict["21:00-21:59"] += 1
            else:
                published_dict["21:00-21:59"] = 1
        elif published_time < datetime.time(23,0,0):
            if "22:00-22:59" in published_dict:
                published_dict["22:00-22:59"] += 1
            else:
                published_dict["22:00-22:59"] = 1
        elif published_time <= datetime.time(23,59,59):
            if "23:00-23:59" in published_dict:
                published_dict["23:00-23:59"] += 1
            else:
                published_dict["23:00-23:59"] = 1


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

    X = []
    y = []
    for key, value in sorted(published_count.items(), key=lambda item: item[0]):
        X.append(key)
        y.append(value)

    plt.bar(np.arange(len(X)), np.array(y), align='center')
    plt.xticks(np.arange(len(X)), np.array(X), rotation='vertical')
    plt.title("Number of Videos Published per Hour")
    plt.xlabel('Published Time')
    plt.ylabel('Number of Videos Published')
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
            if "00:00-00:59" in published_dict:
                published_dict["00:00-00:59"].append(viewCount)
            else:
                published_dict["00:00-00:59"] = [viewCount]
        elif published_time < datetime.time(2,0,0):
            if "01:00-01:59" in published_dict:
                published_dict["01:00-01:59"].append(viewCount)
            else:
                published_dict["01:00-01:59"] = [viewCount]
        elif published_time < datetime.time(3,0,0):
            if "02:00-02:59" in published_dict:
                published_dict["02:00-02:59"].append(viewCount)
            else:
                published_dict["02:00-02:59"] = [viewCount]
        elif published_time < datetime.time(4,0,0):
            if "03:00-03:59" in published_dict:
                published_dict["03:00-03:59"].append(viewCount)
            else:
                published_dict["03:00-03:59"] = [viewCount]
        elif published_time < datetime.time(5,0,0):
            if "04:00-04:59" in published_dict:
                published_dict["04:00-04:59"].append(viewCount)
            else:
                published_dict["04:00-04:59"] = [viewCount]
        elif published_time < datetime.time(6,0,0):
            if "05:00-05:59" in published_dict:
                published_dict["05:00-05:59"].append(viewCount)
            else:
                published_dict["05:00-05:59"] = [viewCount]
        elif published_time < datetime.time(7,0,0):
            if "06:00-06:59" in published_dict:
                published_dict["06:00-06:59"].append(viewCount)
            else:
                published_dict["06:00-06:59"] = [viewCount]
        elif published_time < datetime.time(8,0,0):
            if "07:00-07:59" in published_dict:
                published_dict["07:00-07:59"].append(viewCount)
            else:
                published_dict["07:00-07:59"] = [viewCount]
        elif published_time < datetime.time(9,0,0):
            if "08:00-08:59" in published_dict:
                published_dict["08:00-08:59"].append(viewCount)
            else:
                published_dict["08:00-08:59"] = [viewCount]
        elif published_time < datetime.time(10,0,0):
            if "09:00-09:59" in published_dict:
                published_dict["09:00-09:59"].append(viewCount)
            else:
                published_dict["09:00-09:59"] = [viewCount]
        elif published_time < datetime.time(11,0,0):
            if "10:00-10:59" in published_dict:
                published_dict["10:00-10:59"].append(viewCount)
            else:
                published_dict["10:00-10:59"] = [viewCount]
        elif published_time < datetime.time(12,0,0):
            if "11:00-11:59" in published_dict:
                published_dict["11:00-11:59"].append(viewCount)
            else:
                published_dict["11:00-11:59"] = [viewCount]
        elif published_time < datetime.time(13,0,0):
            if "12:00-12:59" in published_dict:
                published_dict["12:00-12:59"].append(viewCount)
            else:
                published_dict["12:00-12:59"] = [viewCount]
        elif published_time < datetime.time(14,0,0):
            if "13:00-13:59" in published_dict:
                published_dict["13:00-13:59"].append(viewCount)
            else:
                published_dict["13:00-13:59"] = [viewCount]
        elif published_time < datetime.time(15,0,0):
            if "14:00-14:59" in published_dict:
                published_dict["14:00-14:59"].append(viewCount)
            else:
                published_dict["14:00-14:59"] = [viewCount]
        elif published_time < datetime.time(16,0,0):
            if "15:00-15:59" in published_dict:
                published_dict["15:00-15:59"].append(viewCount)
            else:
                published_dict["15:00-15:59"] = [viewCount]
        elif published_time < datetime.time(17,0,0):
            if "16:00-16:59" in published_dict:
                published_dict["16:00-16:59"].append(viewCount)
            else:
                published_dict["16:00-16:59"] = [viewCount]
        elif published_time < datetime.time(18,0,0):
            if "17:00-17:59" in published_dict:
                published_dict["17:00-17:59"].append(viewCount)
            else:
                published_dict["17:00-17:59"] = [viewCount]
        elif published_time < datetime.time(19,0,0):
            if "18:00-18:59" in published_dict:
                published_dict["18:00-18:59"].append(viewCount)
            else:
                published_dict["18:00-18:59"] = [viewCount]
        elif published_time < datetime.time(20,0,0):
            if "19:00-19:59" in published_dict:
                published_dict["19:00-19:59"].append(viewCount)
            else:
                published_dict["19:00-19:59"] = [viewCount]
        elif published_time < datetime.time(21,0,0):
            if "20:00-20:59" in published_dict:
                published_dict["20:00-20:59"].append(viewCount)
            else:
                published_dict["20:00-20:59"] = [viewCount]
        elif published_time < datetime.time(22,0,0):
            if "21:00-21:59" in published_dict:
                published_dict["21:00-21:59"].append(viewCount)
            else:
                published_dict["21:00-21:59"] = [viewCount]
        elif published_time < datetime.time(23,0,0):
            if "22:00-22:59" in published_dict:
                published_dict["22:00-22:59"].append(viewCount)
            else:
                published_dict["22:00-22:59"] = [viewCount]
        elif published_time <= datetime.time(23,59,59):
            if "23:00-23:59" in published_dict:
                published_dict["23:00-23:59"].append(viewCount)
            else:
                published_dict["23:00-23:59"] = [viewCount]

    published_to_viewavg = {published: sum(viewlist)/len(viewlist) for published, viewlist in published_dict.items()}

    x_avg = []
    y_avg = []
    for key, value in sorted(published_to_viewavg.items(), key=lambda item: item[0]):
        x_avg.append(key)
        y_avg.append(value)
        # print("%s: %s" % (key, value))

    # x_avg = list(published_dict.keys())
    # y_avg = [published_to_viewavg[published] for published in x_avg]

    plt.bar(np.arange(len(x_avg)), np.array(y_avg), align='center', color='#2B8CBF')
    plt.xticks(np.arange(len(x_avg)), np.array(x_avg), rotation='vertical')

    plt.title("Average Views per Video for Each Published Time")
    plt.xlabel('Published Time')
    plt.ylabel('Average View Counts')

    plt.show()

if __name__ == '__main__':
    # published_dict()
    published_plot_all()
    duration_plot_averages()
