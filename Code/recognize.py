#!/usr/bin/env python

import pickle
import cv2
import matplotlib.pyplot as plt
import image_search
import os.path
import time
import numpy as np


# Command line parsing is handled by the ArgumentParser object

# Starting point of the script
# =======================================
def recognize_monument(query_images, N, sift_vocabulary):
    """
    Given a list of images, this method will for every frame query the database containing the sift bag of words
    and return a list of monuments and directions based on the top-N results for every query.
    [Code from dbt.py has been used to make this file]

    :param query_images: The frames for which we want to estimate the landmark and the direction
    :param N: The amount of query results we want to take into account
    :param sift_vocabulary: The sift vocabulary (bag of words) to be used to query with, if unspecified (=None),
    the system will use the local one.
    :return: A list of landmarks and a list of directions
    """

    print 'Monument Recognition Tool'
    print '================================\n'
    search = image_search.Searcher('db/invention_sift_DB.db')

    # Load sift vocabulary if needed
    if sift_vocabulary is None:
        print 'Loading SIFT vocabulary ...'
        start_time = time.time()
        fname = 'db/invention_sift_DB_sift_vocabulary.pkl'
        # Load the vocabulary to project the features of our query images on
        with open(fname, 'rb') as f:
            sift_vocabulary = pickle.load(f)
        print 'Loading SIFT vocabulary took', time.time() - start_time, 's'
    print 'Computing SIFT features per query image ...'
    sift = cv2.xfeatures2d.SIFT_create()
    sift_queries = []
    for query_image in query_images:
        kp, desc = sift.detectAndCompute(query_image, None)
        sift_queries.append(desc)

    # Get a histogram of visual words for the query image
    image_words_list = []
    for sift_query in sift_queries:
        image_words_list.append(sift_vocabulary.project(sift_query))
    print 'Query database with a SIFT histogram...'
    # Use the histogram to search the database
    sift_candidates_list = []
    for image_words in image_words_list:
        sift_candidates_list.append(search.query_iw('sift', image_words))

    # # Plot query image
    # fig = plt.figure()
    # query_im = query_image
    # # Convert colorspace from BGR to RGB since we're plotting with pyplot
    # query_im = cv2.cvtColor(query_im, cv2.COLOR_BGR2RGB)
    # plt.imshow(query_im)
    # plt.axis('off')
    # fig.canvas.set_window_title('Query Image')

    def plot_results(im_list, title, distance, labels=None):
        fig = plt.figure()
        i = 1
        for im_name in im_list:
            im_folder = '../Images/inventionimages/'
            im_path = os.path.join(im_folder, os.path.basename(im_name))
            print(im_name)
            im = cv2.imread(im_path, cv2.IMREAD_COLOR)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            plt.subplot(2, 5, i)
            plt.imshow(im)
            if labels == None:
                plt.title(i)
            else:
                plt.title(labels[i - 1])
            plt.axis('off')
            i += 1
        fig.canvas.set_window_title(title)

    # Majority voting to determine which landmark and direction is the most probable
    def majority_vote(results):
        monument_mv = []
        direction_mv = []

        for result in results:
            subs = result.split('_')
            monument_mv.append(subs[2])
            direction_mv.append(subs[1])
            
        monument_mv = np.array(monument_mv)
        direction_mv = np.array(direction_mv)

        monument = np.unique(monument_mv)[-1]
        relevant_directions = direction_mv[monument_mv == monument]
        m_direction = np.unique(relevant_directions)[-1]

        return monument, m_direction


    landmarks = list()
    directions = list()

    # Select the N best sift results
    for sift_candidates in sift_candidates_list:
        sift_winners = [search.get_filename(cand[1]) for cand in sift_candidates][0:N]
        sift_distances = [cand[0] for cand in sift_candidates][0:N]
        # print majority_vote(sift_winners)
        landmark, direction = majority_vote(sift_winners)
        landmarks.append(landmark)
        directions.append(direction)
        # plot_results(sift_winners, 'SIFT Results', sift_distances)

    # # Add Key event to close the application with the 'q' or 'escape' key
    # def onKey(event):
    #     if event.key == 'q' or event.key == 'escape':
    #         sys.exit(0)
    #
    # plt.connect('key_release_event', onKey)
    # plt.show()

    return landmarks, directions


if __name__ == '__main__':
    recognize_monument([cv2.imread('../Images/inventionimages/edt_SW_nk_z_w_toren2.jpg', cv2.IMREAD_COLOR),
                        cv2.imread('../Images/inventionimages/ers_NE_rh_z_m_close.JPG', cv2.IMREAD_COLOR),
                        cv2.imread('../Images/inventionimages/euk_S_oj_p_w_gracht_bij_oj.jpg', cv2.IMREAD_COLOR),
                        cv2.imread('../Images/inventionimages/hoe_S_nk_z_m_kerk2.jpg', cv2.IMREAD_COLOR),
                        cv2.imread('../Images/inventionimages/ing_SW_nk_m_church.jpg', cv2.IMREAD_COLOR)])
