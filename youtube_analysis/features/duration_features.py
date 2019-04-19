import isodate
import numpy as np
import matplotlib.pyplot as plt

from youtube_analysis.videos_getter import query_videos

def isodate_to_secs(ptstr):
    # Args:
    #  ptstr (string): duration in the format PT#M#S
    # Returns:
    #  # seconds the duration string corresponds to (int)
    dur = isodate.parse_duration(ptstr)
    return int(dur.total_seconds())

def duration_dict():
    # Returns:
    #  Dictionary in the form videoid -> duration in seconds

    dur_dict = {}
    duration_results = query_videos("SELECT id, duration FROM videos;")

    for r_tuple in duration_results:
        vid, dur = r_tuple
        dur_dict[vid] = isodate_to_secs(dur)

    return dur_dict

def feature_vector(video_ids):
    duration_vector = [] # ordered list of durations duration

    duration_results = query_videos("SELECT id, duration FROM videos;")

    for r_tuple in duration_results:
        vid, dur = r_tuple
        # check if in video_ids here rather than in query because it's cheaper
        if vid in video_ids:
            duration_vector.append(isodate_to_secs(dur))

    return [duration_vector]

def duration_plot_all():
    # No params or return
    # Plots all durations vs viewCount

    duration_results = query_videos("SELECT id, duration, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    X = []
    y = []

    for r_tuple in duration_results:
        vid, dur, views = r_tuple
        X.append(isodate_to_secs(dur))
        y.append(views)

    plt.scatter(np.array(X), np.array(y), alpha=0.5)
    plt.title('Video durations x view counts')
    plt.xlabel('video duration in seconds')
    plt.ylabel('view counts')
    plt.show()

def duration_plot_averages():
    # No params or return
    # Plots durations vs average viewCount for that duration,
    # and then uses polyfit to draw a polynomial line representing this curve

    duration_results = query_videos("SELECT id, duration, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    dur_to_viewlist = {}

    for r_tuple in duration_results:
        vid, dur, views = r_tuple
        dur_as_secs = isodate_to_secs(dur)
        if dur_as_secs in dur_to_viewlist:
            dur_to_viewlist[dur_as_secs].append(views)
        else:
            dur_to_viewlist[dur_as_secs] = [views]
    dur_to_viewavg = {dur: sum(viewlist)/len(viewlist) for dur, viewlist in dur_to_viewlist.items()}

    x_avg = list(dur_to_viewavg.keys())
    y_avg = [dur_to_viewavg[dur] for dur in x_avg]

    plt.title('Video durations x view counts')
    plt.xlabel('video duration in seconds')
    plt.ylabel('view counts')

    plt.scatter(np.array(x_avg), np.array(y_avg),  alpha=0.5)
    x_restricted = []
    y_restricted = []
    for i, x in enumerate(x_avg):
        if x < 3600: # 1 hour
            x_restricted.append(x)
            y_restricted.append(y_avg[i])
    # polynom_coeffs = np.polyfit(x_restricted, y_restricted, 2)
    # polynom_func = np.poly1d(polynom_coeffs)
    #
    # x_poly = np.linspace(min(x_restricted), max(x_restricted), 50)
    # y_poly = polynom_func(x_poly)
    #
    # plt.plot(np.array(x_poly), np.array(y_poly),  color="orange")
    # plt.show()

if __name__ == '__main__':
    video_to_duration = duration_dict()

    sum_durations = sum(video_to_duration.values())
    n_videos = len(video_to_duration)
    print("total number of seconds in db:", sum_durations)
    print("average number of seconds in db:", sum_durations/n_videos)

    duration_plot_all()
