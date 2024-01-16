'''모듈 3. 추론 관리 
1) Log 파일 생성
2) 추론 결과 
    - YOLOv8
    - BLIP

sce = Abbreviation of scenario.
'''
import os 
import gradio as gr
import cv2
import argparse
import ffmpeg
import time
from PIL import Image
from ultralytics import YOLO

import torch
from lavis.models import load_model_and_preprocess

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('log.out')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
def yolo_infer(file, modelname):
    input_video_url = file.name
    os.makedirs('./video/out', exist_ok=True)

    # model define
    model = YOLO(f'./weights/{modelname}')
    results = model(input_video_url)

    cap = cv2.VideoCapture(input_video_url)
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) 

    video_name = os.path.basename(input_video_url)
    output_path = os.getcwd()+'/video/out/' + video_name
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    for i in range(len(results)):
        result = results[i]
        img = result.plot()

        out.write(img)
    out.release()
    now = time.localtime()
    resized_video = time.strftime('%Y%m%d%H%M%S') + '.mp4'
    ffmpeg.input(output_path).output(resized_video , crf=35).run() # Reduce Video File Size 
    return input_video_url, resized_video

def blip_infer(img_array):
    # image = Image.open(input_img_url).convert("RGB")
    image = Image.fromarray(img_array)

    model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
    image = vis_processors["eval"](image).unsqueeze(0).to(device)
    caption = model.generate({"image": image})

    return caption[0]
