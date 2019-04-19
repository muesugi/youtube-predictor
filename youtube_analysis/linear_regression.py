import numpy as np
from sklearn import linear_model, metrics, model_selection

from videos_getter import query_videos
from youtube_analysis.features import duration_features
from youtube_analysis.features import title_features

# README: THIS WHOLE PAGE IS JUST DRAFTING
# A GOOD SET UP TO USE MULTIPLE REGRESSION ON
# FEATURES FROM DIFFERENT FILES/PROCESSES

# every feature should have a function that looks like this:
# def feature_vector(video_ids):
#    .... query sql, process results ...
#    return a list of ordered lists;
#       ie, [vector1, ... vectorn] where each index of a given vector
#       corresponds to the video at that index in video_ids

def simple_linear_regression(x,y):
    # x and y are 1-D arrays
    x = np_1d_to_2d(x) # make it a "matrix"

    run_regression(x, y)


def multiple_linear_regression(video_ids, feature_funcs, view_counts):
    X = [] # first construct matrix with vectors as rows
    for f in feature_funcs:
        for output_vector in f(video_ids):
            X.append(np.array(output_vector))
    X = np.array(X)

    # since transpose doesn't work on a 1d array,
    # check length to see how to switch rows & columns
    if X.shape[0] == 1: # 1 row; ie, X will eventually have 1 vector
        X = np_1d_to_2d(X)
    else:
        X = np.transpose(X)

    run_regression(X, view_counts)

####### Utility functions #######
def np_1d_to_2d(array):
    # changes a 1d array ([a, b, c]) to a 2d array with one column, [a, b, c]
    return np.reshape(array, (-1, 1))

def run_regression(X, y):
    # assumes a 2d matrix X and 1d matrix y
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=.2)

    reg_model = linear_model.LinearRegression().fit(X_train, y_train)

    print("Training R-squared:", reg_model.score(X_train, y_train))

    y_train_pred = reg_model.predict(X_train)
    y_test_pred = reg_model.predict(X_test)

    print("Training MSE:", metrics.mean_squared_error(y_train, y_train_pred))
    print("Testing MSE:",  metrics.mean_squared_error(y_test, y_test_pred))


if __name__ == '__main__':
    # constrain video ids for all feature_vectors
    vids_and_counts = query_videos("SELECT id, viewCount FROM videos WHERE viewCount IS NOT NULL;")

    video_ids = [tup[0] for tup in vids_and_counts]
    view_counts = [tup[1] for tup in vids_and_counts]

    # Examples
    # 1. Let's try simple linear regression with the duration feature! (probably quite bad, since it's not linear)
    simple_x = duration_features.feature_vector(video_ids)[0]
    simple_y = view_counts

    # simple_linear_regression(simple_x, simple_y)

    # 2. Multiple linear regression with the same thing; underlying calculations should be the same
    # multiple_linear_regression(video_ids, [duration_features.feature_vector], view_counts)

    # 3. Multiple linear regression on top 50 words
    multiple_linear_regression(video_ids, [title_features.smarter_topkstems_feature_vectors], view_counts)
