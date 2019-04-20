import isodate
import numpy as np
import matplotlib.pyplot as plt

from youtube_analysis.videos_getter import query_videos

def category_dict():
    # Returns:
    #  Dictionary in the form videoid -> duration in seconds

    category_dict = {}
    category_results = query_videos("SELECT id, categoryId FROM videos;")

    for r_tuple in category_results:
        vid, cat = r_tuple
        category_dict[vid] = cat

    return category_dict

def feature_vector(video_ids):
    category_vector = []

    category_results = query_videos("SELECT id, categoryId FROM videos;")

    for r_tuple in category_results:
        vid, cat = r_tuple
        # check if in video_ids here rather than in query because it's cheaper
        if vid in video_ids:
            category_vector.append(cat)

    return [category_vector]

def category_plot_all():
    # No params or return
    # Plots all durations vs viewCount

    duration_results = query_videos("SELECT id, categoryId, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    # TODO: get this info from youtube data API
    id_name = {
        1:'Film & Animation',
        2:'Autos & Vehicles',
        10:'Music',
        15:'Pets & Animals',
        17:'Sports',
        18:'Short Movies',
        19:'Travel & Events',
        20:'Gaming',
        21:'Videoblogging',
        22:'People & Blogs',
        23:'Comedy',
        24:'Entertainment',
        25:'News & Politics',
        26:'Howto & Style',
        27:'Education',
        28:'Science & Technology',
        29:'Nonprofits & Activism',
        30:'Movies',
        31:'Anime/Animation',
        32:'Action/Adventure',
        33:'Classics',
        34:'Comedy',
        35:'Documentary',
        36:'Drama',
        37:'Family',
        38:'Foreign',
        39:'Horror',
        40:'Sci-Fi/Fantasy',
        41:'Thriller',
        42:'Shorts',
        43:'Shows',
        44:'Trailers'
    }

    category_count = {}

    for r_tuple in duration_results:
        vid, cat, views = r_tuple
        if cat in category_count:
            category_count[cat] += 1
        else:
            category_count[cat] = 1

    y_pos = np.arange(len(category_count))
    category_ids = list(category_count.keys())
    categories = []

    for id in category_ids:
        categories.append(id_name[id])

    vals = list(category_count.values())

    plt.bar(y_pos, vals, align = 'center', alpha=0.5)
    plt.xticks(y_pos, categories, rotation='vertical')
    plt.xlabel('Category')
    plt.ylabel('Number of Videos')
    plt.show()

def category_plot_averages():
    # No params or return
    # Plots durations vs average viewCount for that duration,
    # and then uses polyfit to draw a polynomial line representing this curve

    category_results = query_videos("SELECT id, categoryId, viewCount FROM videos WHERE viewCount IS NOT NULL;")

        # TODO: get this info from youtube data API
    id_name = {
        1:'Film & Animation',
        2:'Autos & Vehicles',
        10:'Music',
        15:'Pets & Animals',
        17:'Sports',
        18:'Short Movies',
        19:'Travel & Events',
        20:'Gaming',
        21:'Videoblogging',
        22:'People & Blogs',
        23:'Comedy',
        24:'Entertainment',
        25:'News & Politics',
        26:'Howto & Style',
        27:'Education',
        28:'Science & Technology',
        29:'Nonprofits & Activism',
        30:'Movies',
        31:'Anime/Animation',
        32:'Action/Adventure',
        33:'Classics',
        34:'Comedy',
        35:'Documentary',
        36:'Drama',
        37:'Family',
        38:'Foreign',
        39:'Horror',
        40:'Sci-Fi/Fantasy',
        41:'Thriller',
        42:'Shorts',
        43:'Shows',
        44:'Trailers'
    }

    category_to_viewlist = {}

    for r_tuple in category_results:
        vid, category, views = r_tuple
        if category in category_to_viewlist:
            category_to_viewlist[category].append(views)
        else:
            category_to_viewlist[category] = [views]
    category_to_viewavg = {id_name[category]: sum(viewlist)/len(viewlist) for category, viewlist in category_to_viewlist.items()}

    x = list(category_to_viewavg.keys())
    y_avg = [category_to_viewavg[category] for category in x]

    plt.xlabel('Categories')
    plt.ylabel('View Counts')

    y_pos = np.arange(len(y_avg))

    plt.bar(y_pos, y_avg, align = 'center', alpha=0.5)
    plt.xticks(y_pos, x, rotation='vertical')
    plt.xlabel('Category')
    plt.ylabel('Average Number of Views')
    plt.show()

if __name__ == '__main__':
    video_to_category = category_dict()
    category_plot_all()
    category_plot_averages()
