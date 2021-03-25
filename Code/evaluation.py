#!/usr/bin/env python
import argparse
import glob
from video_geolocation_detection import geolocation_detection
import time
import pickle

types = list('*.MOV')


def score(test_videos_path):
    print "System Evaluation"
    print "================="
    video_list = []
    for type_ in types:
        files = test_videos_path + type_
        video_list.extend(glob.glob(files))
    video_list = video_list[:len(video_list) - 1]
    num_videos = len(video_list)
    landmark_score = 0
    direction_score = 0
    sift_vocabulary = None
    print 'Loading SIFT vocabulary ...'
    start_time = time.time()
    fname = 'db/invention_sift_DB_sift_vocabulary.pkl'
    # Load the vocabulary to project the features of our query images on
    with open(fname, 'rb') as f:
        sift_vocabulary = pickle.load(f)
    print 'Loading SIFT vocabulary took', time.time() - start_time, 's'

    for video in video_list:
        print "Testing for", video
        vid_name = video.split('/')
        vid_name = vid_name[len(vid_name)-1]
        vid_name = vid_name.split('_')
        gt_landmark = vid_name[0]
        gt_direction = vid_name[1]

        video_landmark, video_direction = geolocation_detection(video, 30, 5, sift_vocabulary)
        # print "Ground truth:", gt_landmark, gt_direction
        # print "System results:", video_landmark, video_direction
        if gt_landmark == video_landmark:
            landmark_score += 1
        if gt_direction == video_direction:
            direction_score += 1

    print 'Landmark Score = ', landmark_score/float(num_videos)
    print 'Direction Score = ', direction_score/float(num_videos)
    print "================="


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluation for Landmark + Direction recognition")
    parser.add_argument("test_videos", help="Path to test videos")
    args = parser.parse_args()

    score(args.test_videos)

