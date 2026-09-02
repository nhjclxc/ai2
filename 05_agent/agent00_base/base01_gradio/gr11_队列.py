import random

import gradio as gr

import time

from numpy import strings

# 队列
# https://gradio.org.cn/guides/queuing


letter = "qwertyuiopasdfghjklzxcvbnm1234567890"

history = []

with gr.Blocks() as queue_blocks:

    with gr.Row():
        prompt_text = gr.Text()
        btn = gr.Button("btn")
        concurrency_number = gr.Number(interactive=False)

    @gr.render(inputs=[prompt_text], triggers=[btn.click], concurrency_limit=3)
    def gen_text(prompt):
        if prompt is None:
            prompt = ""
        print(f"提交数据： {prompt}")
        stime = time.time()
        # concurrency_number +1
        time.sleep(3)
        # concurrency_number -1

        gtext = ''.join(random.choice(letter) for _ in range(10))
        res_text = prompt + "[" + gtext + "]"

        etime = time.time()
        res = f"start: {stime}, end: {etime}, text: {res_text}"

        history.append(res)
        for r in history:
            gr.Textbox(r)

        return res

queue_blocks.launch()



