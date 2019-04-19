from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

from collections import Counter
import numpy as np

from youtube_analysis.videos_getter import query_videos

def process_title(title, stems_to_ignore=[]):
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
    words_stemmed = [stemmer.stem(w) for w in words_no_stops]

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
    print(smarter_topkstems(video_ids,50))
    print(channeltitle_topkstems(video_ids,50))
