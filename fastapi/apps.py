import shutil
import gradio as gr
import os

from resource_manager import resourceManager
from infer_manager import yolo_infer, blip_infer

rm = resourceManager()

# os.makedirs('./videos', exist_ok=True)
# def uploadfile(file):
#         filename = file.name
#         global save_path
#         save_path = './videos/' + os.path.basename(filename)
#         shutil.copy(filename, save_path)
#         return save_path

def appYolo(object_name, private=None):
    if object_name == "SmartFarm":
        model = gr.Textbox(visible=False, value="y8n_tmt_best.pt") # Tomato
    elif object_name == "SmartCity":
        model = gr.Textbox(visible=False, value="pd_base.pt") # LicensePlate
    else:
        model = gr.Textbox(visible=False, value=private) # private model
    # Gradio UI
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Markdown(f"# {object_name} Detector")
                file1 = gr.File(label="📂", file_types=['.mp4'])
                btn1 = gr.Button("Run", size="sm")
            with gr.Column():
                output2 = gr.Video(autoplay=True) # Play Original Video 
            with gr.Column():
                output3 = gr.Video(autoplay=True) # Play Result Video

            btn1.click(fn=yolo_infer, inputs=[file1, model], outputs=[output2, output3])

        with gr.Row():
                gr.LinePlot(rm.cpu_usg, x="timestamps",y="cpu_percentages",tooltip=["timestamps","cpu_percentages"], title="CPU_usage(%)", every=10)
                gr.LinePlot(rm.gpu_usg, x="timestamps", y="gpu_percentages", tooltip=["timestamps","gpu_percentages"], title="GPU_usage(%)", every=10) # ���� GPU �ó�����
                gr.LinePlot(rm.cpu_usg, x="timestamps", y="used_memory", tooltip=["timestamps","used_memory"], title="Memory_usage",every=10)

def appBlip():
    # Gradio UI
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Markdown(f"# Image Captioning")
                input1 = gr.Image(label = "Image URL") # Put Image URL
                btn1 = gr.Button("Run", size="sm")
            with gr.Column():
                output1 = gr.Textbox(label="Result")
        
        btn1.click(fn = blip_infer, inputs=input1, outputs=output1)

        with gr.Row():
                gr.LinePlot(rm.cpu_usg, x="timestamps",y="cpu_percentages",tooltip=["timestamps","cpu_percentages"], title="CPU_usage(%)", every=10)
                gr.LinePlot(rm.gpu_usg, x="timestamps", y="gpu_percentages", tooltip=["timestamps","gpu_percentages"], title="GPU_usage(%)", every=10) # ���� GPU �ó�����
                gr.LinePlot(rm.cpu_usg, x="timestamps", y="used_memory", tooltip=["timestamps","used_memory"], title="Memory_usage",every=10)
