#!/usr/bin/env python
import argparse
import cv2
import time

from recognize import recognize_monument
from video_landmark_estimation import video_landmark_estimation
from video_tools import get_frame_count


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def geolocation_detection(input_video, sample_amount):
    start_time = time.time()
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print bcolors.FAIL + 'please check your working directory and the path to your input video' + bcolors.ENDC
    else:  # if video capturing has been initialized correctly
        print 'Input video:', bcolors.HEADER + input_video + bcolors.ENDC, '\n'

        frame_count = get_frame_count(input_video) + 1
        n_sample = int(sample_amount)  # the amount of sample frames taken from the input video
        frames_indices = [frame_count / (n_sample + 1) * i for i in range(1, n_sample + 1)]  # uniform distribution

        sample_frames = list()
        for frame_id in frames_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cap.read()
            if ret:  # if frame is read correctly
                sample_frames.append(frame)
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #
                # # show the captured frames
                # cv2.imshow('frame', gray)
                # if cv2.waitKey(10) & 0xFF == ord('q'):
                #     break

        landmark_frames, direction_frames = recognize_monument(sample_frames)
        video_landmark, video_direction = video_landmark_estimation(landmark_frames, direction_frames)
        print 'Estimated landmark:', bcolors.UNDERLINE + bcolors.OKCYAN + video_landmark + bcolors.ENDC
        print 'Direction in which the video was taken:', bcolors.UNDERLINE + bcolors.OKCYAN + video_direction + bcolors.ENDC
        print 'Process Duration:', bcolors.UNDERLINE + bcolors.OKCYAN + str(time.time() - start_time) + bcolors.ENDC, "s"
    cap.release()
    # cv2.destroyAllWindows()
    return video_landmark, video_direction


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Geo-location Predication via Landmarks for Videos")
    parser.add_argument("input_video", help="Path to input video")
    parser.add_argument("-n", help="Amount of sample frames", default=10)
    args = parser.parse_args()

    geolocation_detection(input_video=args.input_video, sample_amount=args.n)
