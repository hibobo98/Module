import argparse
import gradio as gr
import cv2
import os, shutil
import time 
import ffmpeg
from resource_manager import resourceManager
from infer_manager import blip_infer

rm = resourceManager()


os.makedirs('./videos', exist_ok=True)
def uploadfile(file):
    filename = file.name
    save_path = './videos/' + os.path.basename(filename)
    shutil.copy(filename, save_path)
    return save_path

def appBlip():
    # Gradio UI
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                markdown = gr.Markdown(f"# Image Captioning")
                output1 = gr.Image(label = "Image URL") # Put Image URL
                btn1upload = gr.UploadButton("?", type='file')
                btn1 = gr.Button("Run", size="sm")
            with gr.Column():
                output2 = gr.Textbox(label="Result")

        btn1upload.upload(uploadfile, btn1upload, output1)
        btn1.click(fn = blip_infer, inputs=output1, outputs=output2)

        with gr.Row():
                gr.LinePlot(rm.cpu_usg, x="timestamps",y="cpu_percentages",tooltip=["timestamps","cpu_percentages"], title="CPU_usage(%)", every=10)
                gr.LinePlot(rm.gpu_usg, x="timestamps", y="gpu_percentages", tooltip=["timestamps","gpu_percentages"], title="GPU_usage(%)", every=10) # 단일 GPU 시나리오
                gr.LinePlot(rm.cpu_usg, x="timestamps", y="used_memory", tooltip=["timestamps","used_memory"], title="Memory_usage",every=10)

