import argparse
import cv2
import os
from tqdm import tqdm

def getFrameAdvanceCount(inVidCap, timeIntervalSec):
    """
    :param inVidCap: cv2.VideoCapture Instance
    :param timeIntervalSec: Desired Interval of time (seconds)
    :return: Return the number of frame required to advance
             each iteration to match time interval
    """
    fps = int(inVidCap.get(cv2.CAP_PROP_FPS))
    return fps * timeIntervalSec

def write_image_with_exception(outPath, frame):
    """
    cv2.imwrite() method does not raise an exception.
    NOTE: Can this be a decorator?
    :param outPath:
    :param frame:
    :return:
    """
    if not cv2.imwrite(outPath, frame):
        raise Exception("ERROR: Frame failed to write.")

def get_abs_path(in_path):
    """
    Given a relative or absolute path, return the absolute path.
    :param in_path:
    :return:
    """
    if os.path.isabs(in_path):
        return in_path
    else:
        return os.path.abspath(in_path)

if __name__ == '__main__':
    # Define command line interface
    parser = argparse.ArgumentParser(description='Extract frames at a specified interval from an input video.')

    parser.add_argument('input_path', help="Input path to video file.", action="store")
    parser.add_argument('output_path', help="Output directory for extracted frames.", action="store")
    parser.add_argument('--interval', help="Interval (seconds) between frames.",
                        action="store", dest="interval_seconds", type=int, default=5)
    parser.add_argument('--start-time', help="Start time (seconds) for frame extraction.",
                        dest="start_time", type=int, default=0)
    parser.add_argument('--end-time', help="End time (seconds) for frame extraction.",
                        dest="end_time", type=int)
    args = parser.parse_args()

    frame_full_path = get_abs_path(args.output_path)
    if not os.path.exists(frame_full_path):
        raise Exception("Error: Output path does not exist.")

    vid_full_path = get_abs_path(args.input_path)
    vid_file_name = os.path.basename(vid_full_path).split('.')[0]
    if os.path.exists(vid_full_path):
        vidcap = cv2.VideoCapture(vid_full_path)
        # Set video position to desired start time.
        vidcap.set(cv2.CAP_PROP_POS_MSEC, args.start_time*1000)
        frame_advance = getFrameAdvanceCount(vidcap, args.interval_seconds)
    else:
        raise Exception("Error: Input video specified does not exist.")

    # Convert end-time parameter in seconds to frames.
    if not args.end_time:
        final_frame_number = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    else:
        final_frame_number = args.end_time*int(vidcap.get(cv2.CAP_PROP_FPS))

    cur_frame_count = int(vidcap.get(cv2.CAP_PROP_POS_FRAMES))
    # Get number of total iterations for progress bar.
    total_frames = (final_frame_number-cur_frame_count)
    # Setup Progress Par
    pbar = tqdm(total=total_frames)
    while(vidcap.isOpened() and cur_frame_count <= final_frame_number):
        # VideoCapture.read() method returns True/False, and a frame object.
        success, frame = vidcap.read()
        if success:
            out_file_name = vid_file_name + '_' + str(cur_frame_count) + '.jpg'
            out_file_path = os.path.join(args.output_path, out_file_name)
            write_image_with_exception(out_file_path, frame)
            # Advance Frame Counter
            cur_frame_count = cur_frame_count+frame_advance
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, cur_frame_count)
            # Update Progress Bar
            pbar.update(frame_advance)