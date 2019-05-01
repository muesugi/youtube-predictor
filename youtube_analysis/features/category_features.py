import isodate
import numpy as np
import matplotlib.pyplot as plt

from youtube_analysis.videos_getter import query_videos
from math import log10, floor

def category_dict():
    # Returns:
    #  Dictionary in the form videoid -> duration in seconds

    category_dict = {}
    category_results = query_videos("SELECT id, categoryId FROM videos;")

    for r_tuple in category_results:
        vid, cat = r_tuple
        category_dict[vid] = cat

    return category_dict

# feature vector for each category, indices corresponding to which video is in category
def feature_vector(video_ids):
    category_vector = []

    id_name = {1:[], 2:[], 10:[], 15:[], 17:[], 18:[], 19:[], 20:[], 21:[],
    22:[], 23:[], 24:[], 25:[], 26:[], 27:[], 28:[], 29:[], 30:[], 31:[], 32:[],
    33:[], 34:[], 35:[], 36:[], 37:[], 38:[], 39:[], 40:[], 41:[], 42:[], 43:[],
    44:[]}

    category_results = query_videos("SELECT id, categoryId FROM videos;")

    for r_tuple in category_results:
        vid, cat = r_tuple
        for id in id_names:
            if cat == id:
                id_name[id].append(1)
            else:
                id_name[id].append(0)

    return list(id_name.values())

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

    print(category_count[2])

    # del category_count['Autos & Vehicles']
    # del category_count['Nonprofits & Activism']
    # del category_count['Pets & Animals']
    # del category_count['Music']
    # del category_count['Film & Animation']
    # del category_count['Sports']
    # del category_count['Science & Technology']
    # del category_count['News & Politics']

    del category_count[2]
    del category_count[29]
    del category_count[15]
    del category_count[10]
    del category_count[1]
    del category_count[17]
    del category_count[28]
    del category_count[25]

    num_videos = sum(category_count.values())

    categories = []
    def round_to_1(x):
        return round(x, -int(floor(log10(abs(x)))))

    for key, value in category_count.items():
        categories.append(id_name[key] + " " + str(round_to_1((value/num_videos) * 100)) + "%")


    # y_pos = np.arange(len(category_count))
    # category_ids = list(category_count.keys())
    #
    #
    # for id in category_ids:
    #
    #
    vals = list(category_count.values())



    # plt.bar(y_pos, vals, align = 'center', alpha=0.5)
    # plt.xticks(y_pos, categories, rotation='vertical')
    # plt.xlabel('Category')
    # plt.ylabel('Number of Videos')
    # plt.title('Number of Videos per Category')

    patches, texts = plt.pie(vals, startangle=90)

    plt.legend(patches, categories, loc="best")
    plt.axis('equal')
    plt.tight_layout()
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

    plt.bar(y_pos, y_avg, align = 'center')
    plt.xticks(y_pos, x, rotation='vertical')
    plt.xlabel('Category')
    plt.ylabel('Average Number of Views')
    plt.title('Average Number of Views per Video for Each Category')
    plt.show()

if __name__ == '__main__':
    # video_to_category = category_dict()
    category_plot_all()
    category_plot_averages()
