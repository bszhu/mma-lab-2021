import numpy as np


def video_landmark_estimation(landmark_frames, direction_frames):
    """
    Given a list of estimated landmark and direction for each frame, compute
    the best matched landmark and direction for input video by majority voting.

    Parameters
    ----------
    landmark_frames : list of strings
        a list of estimated landmark
    direction_frames : list of strings
        a list of estimated direction

    Returns
    -------
    video_landmark : string
        estimated landmark for input video
    video_direction : string
        estimated direction for input video
    """
    landmark_frames = np.array(landmark_frames)
    direction_frames = np.array(direction_frames)
    video_landmark = np.unique(landmark_frames)[-1]
    # directions corresponding to the estimated landmark
    landmark_directions = direction_frames[landmark_frames == video_landmark]
    video_direction = np.unique(landmark_directions)[-1]
    return video_landmark, video_direction


if __name__ == '__main__':
    l_frames = ['s', 'v', 't', 'v', 't', 'v']
    d_frames = ['S', 'N', 'S', 'N', 'W', 'E']
    landmark_res, direction_res = video_landmark_estimation(l_frames, d_frames)
    print(landmark_res, direction_res)
