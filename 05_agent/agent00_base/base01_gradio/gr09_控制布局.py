
import gradio as gr

# 控制布局
# https://gradio.org.cn/guides/controlling-layout

# 1、使用 with gr.Row 实现行布局
with gr.Blocks() as row_blocks:
    btn1 = gr.Button("btn1")
    btn2 = gr.Button("btn2")
    with gr.Row():
        btn21 = gr.Button("btn21")
        btn22 = gr.Button("btn22")
        text1 = gr.Textbox()

# row_blocks.launch()

# 2、行列嵌套
with gr.Blocks() as row_column_blocks:
    with gr.Row():
        with gr.Column():
            text1 = gr.Textbox()
            btn1 = gr.Button("btn1")

        with gr.Column():
            text2 = gr.Textbox()
            btn2 = gr.Button("btn2")

row_column_blocks.launch()










