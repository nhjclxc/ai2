
import numpy as np
import gradio as gr

# 1、标准输入输出演示

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo1 = gr.Interface(sepia, gr.Image(), "image", api_name="predict")
# demo1.launch()


# 2、仅输出演示
# 实现一个时钟
import time

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

demo2 = gr.Interface(
    fn= current_time,
    inputs= None,
    outputs= ["text"],
    api_name="predict",
)

# demo2.launch()


# 3、仅输入演示
import random
import string

def save_image_random_name(image):
    random_string = ''.join(random.choices(string.ascii_letters, k=20)) + '.png'
    image.save(random_string)
    print(f"Saved image to {random_string}!")

demo3 = gr.Interface(
    fn=save_image_random_name,
    inputs=gr.Image(type="pil"),
    outputs=None,
    api_name="predict",
)

# demo3.launch()


# 4、统一演示
# 一个将单个组件作为输入和输出的演示。只需将 inputs 和 outputs 参数的值设置为相同的组件即可创建。这是一个文本生成模型的示例演示

from transformers import pipeline

generator = pipeline('text-generation', model = 'gpt2')

def generate_text(text_prompt):
  response = generator(text_prompt, max_length = 30, num_return_sequences=5)
  return response[0]['generated_text']

textbox = gr.Textbox()

demo4 = gr.Interface(generate_text, textbox, textbox, api_name="predict")

demo4.launch()



