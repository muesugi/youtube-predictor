from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import random

from youtube_analysis.videos_getter import query_videos

def process_title(title, stems_to_ignore=[], track_stemmed=None):
    # Args:
    #  title (str): title to be processed
    #  stems_to_ignore (optional, list): additional custom stems to ignore
    # processes the title --
    # only conisders alphanumeric, ignores stopwords, and stems all words
    title = title.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(title)

    stop_words = stopwords.words('english')
    words_no_stops = [w for w in words if w not in stop_words]

    stemmer = SnowballStemmer('english')
    words_stemmed = []
    for w in words_no_stops:
        stemmed_w = stemmer.stem(w)
        if track_stemmed is not None:
            if stemmed_w in track_stemmed:
                track_stemmed[stemmed_w].append(w)
            else:
                track_stemmed[stemmed_w] = [w]
        words_stemmed.append(stemmed_w)

    return [stem for stem in words_stemmed if stem not in stems_to_ignore]

def title_topkstems(video_ids, k=10):
    # Returns the top k stems from all relevant video titles

    titles = query_videos("SELECT id, title FROM videos;")
    # assumes titles is a list of tuples, where each tuple contains the title at index 0
    stems_list = []

    for t_tuple in titles:
        vid, t = t_tuple
        if vid in video_ids:
            stems_list.extend(process_title(t))

    return Counter(stems_list).most_common(k)

def smarter_topkstems(video_ids, k=10):
    # Like topkstems, returns the top k stems from all relevant video titles,
    # but omits the channel title from the considered stems

    custom_ignore_stems = ["com"] # stems to ignore across all channels

    titles = query_videos("SELECT id, channelTitle, title FROM videos;")
    # assumes titles is a list of tuples, where each tuple contains the title at index 0
    stems_list = []

    for vid_tuple in titles:
        vid, channelTitle, title = vid_tuple
        if vid in video_ids:
            channelTitleProcessed =  process_title(channelTitle)
            stems_list.extend(process_title(title, stems_to_ignore=custom_ignore_stems + channelTitleProcessed))

    return Counter(stems_list).most_common(k)

def smarter_topkstems(video_ids, k=10):
    # Like topkstems, returns the top k stems from all relevant video titles,
    # but omits the channel title from the considered stems

    custom_ignore_stems = ["com", "sarah", "carey", "vital"] # stems to ignore across all channels

    stem_to_full_words = {}

    titles = query_videos("SELECT id, channelTitle, title FROM videos;")
    # assumes titles is a list of tuples, where each tuple contains the title at index 0
    stems_list = []

    for vid_tuple in titles:
        vid, channelTitle, title = vid_tuple
        if vid in video_ids:
            channelTitleProcessed =  process_title(channelTitle)
            stems_list.extend(process_title(title,
                stems_to_ignore=custom_ignore_stems + channelTitleProcessed,
                track_stemmed=stem_to_full_words))

    return stem_to_full_words, Counter(stems_list).most_common(k)

def plot_smarter_topkstems(stem_to_words, common_stem_counter):
    fig, ax = plt.subplots()
    size = 0.3

    plt.rcParams['font.size'] = 6
    categorized_stems = {
        "Meal Type": ['dessert'],
        "Dish Type": ['cake',  'salad', 'cooki', 'pizza', 'sauc',  'bread',  'soup', 'sandwich', 'curri',  'pasta', 'roll',  'pie',  'pork',  'veget',  'stuf', 'burger'],
        "Ingredient": [ 'chicken',  'chocol',  'chees',  'potato',  'egg',  'ice',  'cream',  'rice', 'fish',  'beef',  'masala',  'paneer',  'bacon'],
        "Cooking Style": ['fri', 'bake', 'grill',  'roast'],
        "World Cuisine": [ 'indian' ],
        "Verb": ['make', 'cook',  'eat'],
        "Adjective": ['easi',  'homemad', 'special',  'sweet',  'best',  'spici', 'quick'],
        "Other": [ 'style', 'recip',  'episod',  'chef',  'kitchen', 'food', ]
    }
    category_list = categorized_stems.keys()

    # category_colors = {cat: "#%06x" % random.randint(0, 0xFFFFFF) for cat in category_list}
    mycolors =  ['#000000', '#55415f', '#646964', '#d77355', '#508cd7', '#64b964', '#e6c86e', '#dcf5ff']
    category_colors = {cat: mycolors[i] for i, cat in enumerate(category_list)}
    print(category_colors)

    stem_list = []
    stem_counts = []
    stem_colors = []
    common_stem_counter = Counter({stem: count for stem, count in common_stem_counter})
    for cat in category_list:
        for stem in categorized_stems[cat]:
            stem_list.append(stem)
            stem_counts.append(common_stem_counter[stem])
            stem_colors.append(category_colors[cat])

    ax.pie(stem_counts, radius=1, colors=stem_colors,
           wedgeprops=dict(width=size, edgecolor='w'),
           labels=stem_list, labeldistance=1.05,
           rotatelabels=True, counterclock=False)
    # get every first patch of each category so we can get the right colors:
    category_patches = [Patch(facecolor=category_colors[cat], edgecolor='w',
                         label=cat) for cat in category_list]

    plt.legend(category_patches, category_list, loc="center")
    ax.set_title('Top 50 Stems In Video Titles By Category',fontsize= 10)
    # ax.set(aspect="equal", title='Top 50 Words In Video Titles By Category')
    plt.tight_layout()
    plt.show()

def smarter_topkstems_feature_vectors(video_ids, k=50):
    custom_ignore_stems = ["com"] # stems to ignore across all channels

    titles = query_videos("SELECT id, channelTitle, title FROM videos;")

    vid_to_stems = {}

    for vid_tuple in titles:
        vid, channelTitle, title = vid_tuple
        if vid in video_ids:
            channelTitleProcessed = process_title(channelTitle)
            title_stems = process_title(title, stems_to_ignore=custom_ignore_stems + channelTitleProcessed)
            vid_to_stems[vid] = title_stems

    # collapse all values in vid_to_stems to a single list of all stems
    stems_list = [stem for stemlist in vid_to_stems.values() for stem in stemlist]
    top_stems = Counter(stems_list).most_common(k)

    # create the vectors!
    feature_vecs = []
    for stem in top_stems:
        # binary feature of whether a given word is in the stems
        feature_vec = [1 if stem in vid_to_stems[v] else 0 for v in video_ids]
        feature_vecs.append(feature_vec)

    return feature_vecs


def channeltitle_topkstems(video_ids, k=10, remove_single_occ=True):
    # returns the top stems from all (unique) channel titles; returns no more than k stems.
    # by default, returns only stems that have occurence greater than 1, so there may be less than k stems

    # > has to be unique bc then that'll just return stems of channel names w most uploads
    titles = query_videos("SELECT DISTINCT channelTitle FROM videos;")
    # assumes titles is a list of tuples, where each tuple contains the title at index 0
    stems_list = []

    for t_tuple in titles:
        t = t_tuple[0]
        stems_list.extend(process_title(t))

    kmostcommon = Counter(stems_list).most_common(k)
    if not remove_single_occ:
        return kmostcommon
    else:
        return [(stem, count) for stem, count in kmostcommon if count > 1]


if __name__ == '__main__':
    video_ids = [tup[0] for tup in query_videos("SELECT id FROM videos;")]
    stem_to_words, common_stem_counter = smarter_topkstems(video_ids,50)
    print(common_stem_counter)
    plot_smarter_topkstems(stem_to_words, common_stem_counter)
    # print(channeltitle_topkstems(video_ids,50))
