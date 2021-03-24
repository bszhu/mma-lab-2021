#!/usr/bin/env python
import argparse
import glob
from video_geolocation_detection import geolocation_detection

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

    for video in video_list:
        print "Testing for", video
        vid_name = video.split('/')
        vid_name = vid_name[len(vid_name)-1]
        vid_name = vid_name.split('_')
        gt_landmark = vid_name[0]
        gt_direction = vid_name[1]
        video_landmark, video_direction = geolocation_detection(video, 10)
        if gt_landmark == video_landmark:
            landmark_score += 1
        if gt_direction == video_direction:
            direction_score += 1

    print 'Landmark Score = ', landmark_score/num_videos
    print 'Direction Score = ', direction_score/num_videos
    print "================="


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluation for Landmark + Direction recognition")
    parser.add_argument("test_videos", help="Path to test videos")
    args = parser.parse_args()

    score(args.test_videos)

