import isodate
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from youtube_analysis.videos_getter import query_videos

##### Interpret and Store Query Results (query results -> Duration objects) #######
class Duration:
    # note the reordering of args from the stanard, to accept non-isodate durations
    def __init__(self, vid, views, dur_as_isodate=None, duration_int=None):
        self.id = vid
        if duration_int:
            self.duration = duration_int
        else:
            self.duration = isodate_to_secs(dur_as_isodate)
        self.viewCount = views

    def __str__(self):
        return 'id: {0}, duration (secs): {1}, views: {2}'.format(
            self.id, self.duration, self.viewCount)

    def __repr__(self):
        return str(self)

def isodate_to_secs(ptstr):
    # Args:
    #  ptstr (string): duration in the format PT#M#S
    # Returns:
    #  # seconds the duration string corresponds to (int)
    dur = isodate.parse_duration(ptstr)
    return int(dur.total_seconds())

def interpret_query_results(duration_results_from_query):
    # Returns:
    #  list of Duration objects with id, duration, and viewcount
    return [ Duration(vid, views, dur) for vid, dur, views in duration_results_from_query]

##### Process Duration Objects (Duration objects -> Duration objects) #####
def filter_durations(duration_objects, video_ids=None, dur_cutoff=None, views_cutoff=None):
    # filter duration object with one or more filters. All are optional.
    def myfilter(d):
        keep = True

        # in video ids
        keep = keep and (video_ids is None or d.id in video_ids)
        if not keep:
            print("filtering out a video id:", d.id)

        # under duration cutoff
        keep = keep and (dur_cutoff is None or d.duration <= dur_cutoff)

        # under views cutoff if applicable
        keep = keep and (views_cutoff is None or d.viewCount <= views_cutoff)

        # can add more here!

        return keep

    return list(filter(myfilter, duration_objects))

def grouped_durations(duration_objects, max_duration=3600, n_groups=30, show_plot=True):
    # take a bunch of duration objects and group them by duration, into n_groups equal groups
    buckets = np.linspace(0, max_duration, n_groups)

    grouped_duration_objects = []

    # buckets contain durations
    # bucket_min < (all durations in bucket) <= bucket_max
    for i in range(len(buckets) - 1):
        x_min = buckets[i] # exclusive
        x_max = buckets[i + 1]

        bucket_duration = (x_min + x_max) / 2
        bucket_views = []

        for dobj in duration_objects:
            if x_min < dobj.duration and dobj.duration <= x_max:
                bucket_views.append(dobj.viewCount)

        avg_bucket_views = 0 if len(bucket_views) == 0 else sum(bucket_views) / len(bucket_views)

        grouped_duration_objects.append(
            Duration(None, avg_bucket_views, duration_int=bucket_duration)
        )

    return grouped_duration_objects

##### Calculate Points from Duration Objects (Duration objects -> (one or more x, one or more y)) #######
def points_from_durations(duration_objects):
    # returns x and y from a list of duration objects
    x = []
    y = []

    for d in duration_objects:
        x.append(d.duration)
        y.append(d.viewCount)

    return np.array(x), np.array(y)

def points_for_polynomial_curve(duration_objects, degree=4):
    # returns the points for a polynomial curve fitted to duration objects

    x, y = points_from_durations(duration_objects)
    polynom_coeffs = np.polyfit(x, y, degree)
    polynom_func = np.poly1d(polynom_coeffs)

    # use the estimated curve to get new points
    x_poly = np.linspace(min(x), max(x), 50)
    y_poly = polynom_func(x_poly)

    return x_poly, y_poly

def peak_point(duration_objects):
    # calls points_for_polynomial_curve and gets the x, y of the peak point
    x_poly, y_poly = points_for_polynomial_curve(duration_objects)

    # gets duration with heighest avg view count
    peak_index = np.argmax(y_poly)
    return x_poly[peak_index], y_poly[peak_index]


##### Plot Duration Objects (one or more x, one or more y -> None; plots) #####
# for all, kwargs passes any extra named args (color, alpha, etc) to the plotting func itself

def plot_scatter(x, y, show_plot=True, **kwargs):
    plt.scatter(x, y, **kwargs)
    plt.title('Video Duration x Average View Count')
    plt.xlabel('video duration in seconds')
    plt.ylabel('view counts')
    if show_plot:
        plt.show()

def plot_bars(x, heights, width, show_plot=True, **kwargs):
    plt.bar(x, heights, width=width, **kwargs)
    plt.title('Grouped Video Durations x Average View Count')
    plt.xlabel('video duration in seconds')
    plt.ylabel('view counts')
    if show_plot:
        plt.show()

def plot_curve(x_poly, y_poly, show_plot=True, **kwargs):
    plt.plot(x_poly, y_poly,  **kwargs)
    if show_plot:
        plt.show()

def plot_point(x, y, show_plot=True, **kwargs):
    plt.plot([x], [y], **kwargs)
    if show_plot:
        plt.show()

##### feature vectors: use from linear_regression #####
def feature_vector__plain_duration(video_ids=None):
    duration_results = query_videos("SELECT id, duration, viewCount FROM videos WHERE viewCount IS NOT NULL;")
    duration_objects = interpret_query_results(duration_results)
    video_id_objects = filter_durations(duration_objects, video_ids=video_ids)

    feature_vector = [d.duration for d in video_id_objects]
    return [feature_vector]

def feature_vector__distance_to_peak(video_ids=None):
    duration_results = query_videos("SELECT id, duration, viewCount FROM videos WHERE viewCount IS NOT NULL;")
    duration_objects = interpret_query_results(duration_results)
    video_id_objects = filter_durations(duration_objects, video_ids=video_ids)
    # print("testing feature vector,len(duration_objects), video_id_objects)

    peak_x, _ = peak_point(video_id_objects)

    feature_vector = [abs(peak_x - video.duration) for video in video_id_objects]
    return [feature_vector]


if __name__ == '__main__':
    duration_results = query_videos("SELECT id, duration, viewCount FROM videos WHERE viewCount IS NOT NULL;")
    duration_objects = interpret_query_results(duration_results)
    filtered_objects = filter_durations(duration_objects, dur_cutoff=3600)
    grouped_durations = grouped_durations(filtered_objects)

    # Generate Points:
    x_scatter, y_scatter = points_from_durations(filtered_objects)
    x_grouped, y_grouped =  points_from_durations(grouped_durations)
    x_poly, y_poly = points_for_polynomial_curve(grouped_durations)
    peak_x, peak_y = peak_point(grouped_durations)

    # Plot Points
    # plot_scatter(x_scatter, y_scatter, alpha=0.2,  show_plot=False) # uncommment to see all points, not just groups
    plot_bars(x_grouped, y_grouped, width=x_poly[0]*2, edgecolor="black", color="w", show_plot=False)
    plot_curve(x_poly, y_poly, color="orange", show_plot=False)
    plot_point(peak_x, peak_y , marker='o', markersize=5, color="firebrick", show_plot=False)

    # plt.show()

    print(feature_vector__distance_to_peak())
