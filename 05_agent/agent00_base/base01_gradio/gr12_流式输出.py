import time

import gradio as gr
import random

import numpy as np

# 流式输出
# https://gradio.org.cn/guides/streaming-outputs

# 可以向 Gradio 提供一个生成器函数，而不是一个常规函数。
# 在 Python 中创建生成器非常简单：函数不是返回单个return值，而是应该yield一系列值。
# 通常，yield语句放在某种循环中。这是一个生成器示例，它只是简单地计数到给定数字

history = []


def gen_num(num, min, max):
    for _ in range(int(num)):
        gen_num = random.randint(int(min), int(max))
        history.append(gen_num)
        yield ", ".join(str(x) for x in history)
        time.sleep(1)

gen_ = gr.Interface(
    fn=gen_num,
    inputs=[gr.Slider(minimum=1, maximum=10, step=1),gr.Slider(minimum=1, maximum=33, step=1),gr.Slider(minimum=1, maximum=33, step=1)],
    outputs="text",
    api_name="predict"
)
# gen_.launch()


def fake_diffusion(steps):
    rng = np.random.default_rng()
    for i in range(steps):
        time.sleep(1)
        image = rng.random(size=(600, 600, 3))
        yield image
    image = np.ones((1000,1000,3), np.uint8)
    image[:] = [255, 124, 0]
    yield image

demo = gr.Interface(fake_diffusion,
                    inputs=gr.Slider(1, 10, 3, step=1),
                    outputs="image",
                    api_name="predict")

# demo.launch()


# 流媒体
# Gradio 可以直接从您的生成器函数流式传输音频和视频。这使得您的用户几乎可以在您的函数yield音频或视频时立即听到或看到它。您需要做的就是：
#
# 在gr.Audio或gr.Video输出组件中设置streaming=True。
# 编写一个 Python 生成器，它逐个“块”地生成音频或视频。
# 设置autoplay=True以便媒体自动开始播放。
# 对于音频，下一个“块”可以是.mp3或.wav文件，也可以是音频的bytes序列。对于视频，下一个“块”必须是.mp4文件或具有h.264编解码器且扩展名为.ts的文件。为了实现流畅播放，请确保块长度一致且大于 1 秒。


def keep_repeating(audio_file):
    for _ in range(10):
        time.sleep(0.5)
        yield audio_file

gr.Interface(keep_repeating,
             gr.Audio(sources=["microphone"], type="filepath"),
             gr.Audio(streaming=True, autoplay=True)
).launch()


def keep_repeating(video_file):
    for _ in range(10):
        time.sleep(0.5)
        yield video_file

gr.Interface(keep_repeating,
     gr.Video(sources=["webcam"], format="mp4"),
     gr.Video(streaming=True, autoplay=True)
).launch()

