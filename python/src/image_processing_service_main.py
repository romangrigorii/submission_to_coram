import argparse
import os
from PIL import Image
import numpy as np
from utils import *
import zmq 
import threading

server = "tcp://*:9876"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(server)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_folder", type=str, required=True)
    return parser.parse_args()

image_proc = [0,0]

def image_proc_stats():
    threading.Timer(1, image_proc_stats).start()
    print(f"Processing images as rate: {image_proc[1] - image_proc[0]} images/s")
    image_proc[0] = image_proc[1]

def main() -> None:
    args = parse_args()
    
    print(f"Binded to clasifier server: {server}")
    print("Streaming classification data.")
    image_proc_stats()
    while(1):
        message = socket.recv()
        # print(f"Received request: {message}")
        if message == b'Classify latest image':
            files = [os.path.join(args.log_folder, file) for file in os.listdir(args.log_folder)]
            if len(files)>0:
                latest_file = max(files, key=os.path.getctime)
                im=np.asarray(Image.open(os.path.join(args.log_folder, latest_file)))
                class_label = classify_image(im)
                socket.send_string(str(class_label))
                image_proc[1]+=1
            else:
                print(f"No images avalable to process")
                socket.send_string("")

if __name__ == "__main__":
    main()


