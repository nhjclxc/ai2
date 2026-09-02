

import gradio as gr

# 使用渲染装饰器（Render Decorator）创建动态应用，动态创建gr的组件
# https://gradio.org.cn/guides/dynamic-apps-with-render-decorator


# 1、动态数量的组件
with gr.Blocks() as dy_compoment:
    in_text = gr.Textbox(label="input")

    # 创建一个@gr.render装饰器，inputs为in_text表示in_text组件内容发生变化时，就会触发这个装饰器函数，进而改变页面行为
    # @gr.render(inputs=in_text)
    @gr.render(inputs=in_text, triggers=[in_text.submit])
    def in_text_rendered(text):
        if len(text) == 0:
            gr.Markdown("# no input text")
        else:
            # gr.Markdown("# input text: "+ text)
            for letter in text:
                gr.Textbox(letter)


dy_compoment.launch()
#

with gr.Blocks() as demo:
    input_text = gr.Textbox(label="input")
    mode = gr.Radio(["textbox", "button"], value="textbox")

    @gr.render(inputs=[input_text, mode], triggers=[input_text.submit])
    def show_split(text, mode):
        if len(text) == 0:
            gr.Markdown("## No Input Provided")
        else:
            for letter in text:
                if mode == "textbox":
                    gr.Textbox(letter)
                else:
                    gr.Button(letter)

# demo.launch()







