'''20240109_blueprint
# TODO 확인해라 
# pip install https://gradio-builds.s3.amazonaws.com/e00ebfb5de9e25c4a29bcec7a8e11b0d23d2861f/gradio-3.39.0-py3-none-any.whl
'''
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import argparse
import gradio as gr
import os, shutil
from resource_manager import resourceManager
from apps import *

clean_theme = gr.Theme.from_hub('freddyaboulton/this-theme-does-not-exist-2')
templates = Jinja2Templates(directory="./")
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name="static")

model_list = []
rm = resourceManager()
os.makedirs('./weights', exist_ok=True) # 없을 경우에만 생성


def uploadfile(file):
    filename = file.name
    save_path = './weights/' + os.path.basename(filename)
    shutil.copy(filename, save_path)
    return save_path

def same(none):
    return none


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale = 0.6):
            markdown1 = gr.Markdown("# Smart Farm 🍅")
            sample1 = gr.Video("./sample/tomato_sample.mp4", autoplay=True) 
            btn1 = gr.Button("Deploy", link="http://127.0.0.1:8000/smartfarm")
        with gr.Column(scale = 0.4):
            markdown3 = gr.Markdown("# Image Captioning")
            sample3 = gr.Image("./sample/img2caption_sample.jpg")
            btn3 = gr.Button("Deploy", link="http://127.0.0.1:8000/caption")
    
    with gr.Row():
        with gr.Column(scale = 0.6):
            markdown2 = gr.Markdown(" # Smart City 🏙 ")
            sample2 = gr.Video("./sample/plate_sample.mp4", autoplay=True) 
            btn2 = gr.Button("Deploy", link="http://127.0.0.1:8000/smartcity")

        with gr.Column(scale = 0.4):
            markdown4 = gr.Markdown("# Upload Your Model")
            textbox4 = gr.Textbox(label="Directory")
            btn4upload = gr.UploadButton("📂", type='file')
            btn4 = gr.Button("Deploy", link="http://127.0.0.1:8000/yourmodels")

            # aaaaab = gr.Interface(appYolo, textbox4, None)

    # Define Button's Functions
    btn4upload.upload(uploadfile, btn4upload, textbox4)

    gr.Markdown("# Resouce Monitoring")
    with gr.Row():
        gr.LinePlot(rm.cpu_usg, x="timestamps",y="cpu_percentages",tooltip=["timestamps","cpu_percentages"], title="CPU_usage(%)", every=10)
        gr.LinePlot(rm.gpu_usg, x="timestamps", y="gpu_percentages", tooltip=["timestamps","gpu_percentages"], title="GPU_usage(%)", every=10) # 단일 GPU 시나리오
        gr.LinePlot(rm.cpu_usg, x="timestamps", y="used_memory", tooltip=["timestamps","used_memory"], title="Memory_usage",every=10)

# First page 
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

with gr.Blocks() as smartfarm:
    appYolo("SmartFarm")
with gr.Blocks() as smartcity:
    appYolo("SmartCity")
with gr.Blocks() as caption:
    appBlip()
with gr.Blocks() as yourmodels:
    pass
    # btn4.click(appYolo, inputs= ["Your own model", textbox4], outputs=None)

app = gr.mount_gradio_app(app, smartfarm, path="/smartfarm")
app = gr.mount_gradio_app(app, smartcity, path="/smartcity")
app = gr.mount_gradio_app(app, caption, path="/caption")
app = gr.mount_gradio_app(app, yourmodels, path="/yourmodels")
# app = gr.mount_gradio_app(app, aaaaab, path="/yourmodels")

smartfarm.queue()
smartcity.queue()
caption.queue()
yourmodels.queue()
demo.queue()
app = gr.mount_gradio_app(app, demo, path='/demo')
 

#     demo.queue().launch(
#     server_name=args.server_name,
#     server_port=args.server_port,
#     debug=True
# )
    
