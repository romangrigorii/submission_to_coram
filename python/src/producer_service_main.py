import argparse
from os.path import isfile,join
from cv2 import VideoCapture as VC
import cv2, os
import os.path, ctypes, sys, pathlib
import time

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file", type=str, required=True)
    parser.add_argument("--log_folder", type=str, required=True)
    return parser.parse_args()

def clean_dir(directory: str) -> None:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    if not os.path.isdir(directory):
        return
    os.chmod(directory, 0o777)
    pathlib.Path(directory).unlink()
    os.mkdir(directory)

def video_to_image_convert(video_path: str, output_dir: str, fps: float) -> None:
    if isfile(join(video_path)):
        print("Converting video to images: ", video_path)
    else:
        print("Video cannot be found. ")
        return
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    cap = VC(video_path)
    # setting up downsampling frames
    vid_fps = float(cap.get(cv2.CAP_PROP_FPS))
    if vid_fps<fps:
        print(f"Sampling video too fast, maximum allow fps is {vid_fps}")
        return
    else:
        print(f"Video being resampled {vid_fps} -> {fps}")
    vid_frame_dt = 1/vid_fps
    image_dt = 1/fps
    time_ticker = 0.0
    iter_max = iter = 0
    out_success, frame = cap.read()
    while out_success:
        ts = time.time()
        time_ticker += vid_frame_dt
        if time_ticker >= image_dt:
            time_ticker%=image_dt  
            cv2.imwrite(os.path.join(output_dir, f'{iter}.png'), frame)
            iter+=1
        iter_max +=1
        out_success, frame = cap.read()
        time.sleep(vid_frame_dt - time.time() + ts)
        time.sleep(.5)

    print(f"Saved {iter}/{iter_max} images.")
    cap.release()
    cv2.destroyAllWindows()

def main() -> None:
    args = parse_args()
    video_to_image_convert(video_path=args.video_file, output_dir=args.log_folder, fps = 15.0)
    pass


if __name__ == "__main__":
    main()
