

import gradio as gr


# 1、数据实时更新

def cul(num1, opt, num2):
    match opt:
        case "add":
            return num1 + num2
        case "sub":
            return num1 - num2
    return 1

web = gr.Interface(
    fn = cul,
    inputs = ["number", gr.Radio(choices=["add", "sub"]), "number"],
    outputs = ["number"],
    # live参数，一旦输入发送变化，就会把输入数据提交，直接会输出输出数据
    live=True,
    api_name="predict",
)

# web.launch()


# 2、流式组件
# 一些组件具有“流式传输”模式，例如麦克风模式下的 Audio 组件，或网络摄像头模式下的 Image 组件。
# 流式传输意味着数据会持续发送到后端，并且 Interface 函数会持续重新运行。

import numpy as np

def flip(im):
    return np.flipud(im)

stream = gr.Interface(
    flip,
    # inputs= gr.Image(sources=["webcam"], streaming=True),
    # outputs="image",
    inputs=gr.Image(),
    outputs=gr.Image(streaming=True),
    live=True,
    api_name="predict",
)

stream.launch()

# 实时语音识别：https://gradio.org.cn/guides/real-time-speech-recognition
