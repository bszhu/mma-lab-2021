#!/usr/bin/env python
import argparse
import glob
from video_geolocation_detection import geolocation_detection
import time
import pickle

types = list('*.3gp')
sample_rates = [10, 40, 60, 100]
top_N = [1, 3, 5, 10]



def train(train_videos_path):
    """
    Training method of the geomatch system

    :param train_videos_path: The path containing the videos for training, the title of the videos should
    contain the landmark (ll) and the direction (dd). Format : ll_dd_xx.3gp (xx --> does not matter)
    :return: Sample rate and top-N sift results that obtained the best score
    """
    print "System Training"
    print "================="

    print "Training with:"
    print "Sample rates =", sample_rates
    print "Top-N for sift =", top_N

    # Load training videos
    video_list = []
    for type_ in types:
        files = train_videos_path + type_
        video_list.extend(glob.glob(files))
    video_list = video_list[:len(video_list) - 1]

    num_videos = len(video_list)
    max_score = 0
    max_s = 0
    max_n = 0

    scores = []
    s_n = []

    print 'Loading SIFT vocabulary ...'
    start_time = time.time()
    fname = 'db/invention_sift_DB_sift_vocabulary.pkl'
    # Load the vocabulary to project the features of our query images on
    with open(fname, 'rb') as f:
        sift_vocabulary = pickle.load(f)
    print 'Loading SIFT vocabulary took', time.time() - start_time, 's'

    print 'Start training session'
    for s in sample_rates:
        for n in top_N:
            landmark_score = 0
            direction_score = 0
            for video in video_list:
                vid_name = video.split('/')
                vid_name = vid_name[len(vid_name)-1]
                vid_name = vid_name.split('_')
                gt_landmark = vid_name[0]
                gt_direction = vid_name[1]

                video_landmark, video_direction = geolocation_detection(video, s, n, sift_vocabulary)
                # print "Ground truth:", gt_landmark, gt_direction
                # print "System results:", video_landmark, video_direction
                if gt_landmark == video_landmark:
                    landmark_score += 1
                if gt_direction == video_direction:
                    direction_score += 1

            print 'Landmark Score = ', landmark_score/float(num_videos)
            print 'Direction Score = ', direction_score/float(num_videos)
            scores.append((landmark_score/float(num_videos), direction_score/float(num_videos)))
            s_n.append((s, n))
            if landmark_score + direction_score / float(num_videos) > max_score:
                max_score = landmark_score + direction_score / float(num_videos)
                max_s = s
                max_n = n
    print 'Best score achieved =', max_score
    print 'Variables used for sample rate and top-N =', max_s, max_n
    print 'All results = ', scores
    print  'For:', s_n
    print "================="

    return max_s, max_n


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Training for Landmark + Direction recognition")
    parser.add_argument("training_videos", help="Path to training videos")
    args = parser.parse_args()

    train(args.training_videos)
