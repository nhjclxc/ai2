

import gradio as gr


# gr.Interface 是 gr.Blocks() 的高度封装
# 当需要有自定义的情况时，使用 gr.Blocks() 来自定义页面布局


def greet(name):
    return "Hello " + name + "!"

# gr.Interface(
#     fn=greet,
#     inputs=["text"],
#     outputs=["text"],
#     api_name="greet"
# ).launch()


with gr.Blocks() as block:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    # 默认情况output组件不支持编辑输出内容，因此可以使用interactive来设置interactive可编辑
    # output = gr.Textbox(label="Output", interactive=True)
    greet_btn = gr.Button("Greet")
    # 使用 greet_btn.click 来实现
    # greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")
    # 也可以使用gr提供的click装饰器来实现对函数的调用
    @greet_btn.click(inputs=name, outputs=output, api_name="greet")
    def greet_btn_clicked(name):
        return "Hello greet_btn_clicked: " + name + "!"

# block.launch()


# change事件类型
def change_func(i):
    return f"this is change_func: {i}"

with gr.Blocks() as change_blocks:
    gr.Markdown("""
    # Markdown wendang
    """)
    input_box = gr.Textbox(label="input box", placeholder="What is your name?")
    output = gr.Textbox(label="Output Box")
    # input_box.change 定义哪个组件来触发事件，input_box.change即表示 input_box 这个组件变化后触发这个事件
    # inputs=input_box 表示事件被触发后的输入是什么
    input_box.change(fn=change_func, inputs=input_box, outputs=output)

# change_blocks.launch()


# 多数据流
def increase(num):
    return num + 1

with gr.Blocks() as increase_blocks:

    a = gr.Number(label="A")
    b = gr.Number(label="B")
    abtn = gr.Button("a > b")
    bbtn = gr.Button("b > a")

    abtn.click(fn=increase, inputs=a, outputs=b)
    bbtn.click(fn=increase, inputs=b, outputs=a)

# increase_blocks.launch()

# 多数据流示例2
# 语音 -> 文本 -> 情感分类 -> 任务心情

def voice2text(voice):
    return f"voice2text: {voice}"

def text2emotion(text):
    return f"text2emotion: {text}"

def emotion2mood(emotion):
    return f"emotion2mood: {emotion}"

with gr.Blocks() as mult_blocks:
    voice_input = gr.Text(label="voice_input")
    text_input = gr.Text(label="text_input", interactive=False)
    emotion_input = gr.Text(label="emotion_input", interactive=False)
    mood_input = gr.Text(label="mood_input", interactive=False)

    btn = gr.Button("button")
    btn.click(fn=voice2text, inputs=voice_input, outputs=text_input)
    text_input.change(fn=text2emotion, inputs=text_input, outputs=emotion_input)
    emotion_input.change(fn=emotion2mood, inputs=emotion_input, outputs=mood_input)

    # 用 Gradio 的事件链写
    # btn.click(
    #     fn=voice2text,
    #     inputs=voice_input,
    #     outputs=text_input
    # ).then(
    #     fn=text2emotion,
    #     inputs=text_input,
    #     outputs=emotion_input
    # ).then(
    #     fn=emotion2mood,
    #     inputs=emotion_input,
    #     outputs=mood_input
    # )

# mult_blocks.launch()



# 函数输入列表与集合

with gr.Blocks() as demo1:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    with gr.Row():
        add_btn = gr.Button("Add")
        sub_btn = gr.Button("Subtract")
    c = gr.Number(label="sum")

    def add(num1, num2):
        return num1 + num2
    add_btn.click(add, inputs=[a, b], outputs=c)

    def sub(data):
        return data[a] - data[b]
    sub_btn.click(sub, inputs={a, b}, outputs=c)

# demo1.launch()

with gr.Blocks() as demo2:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    add_btn = gr.Button("Add")
    sub_btn = gr.Button("Subtract")
    c = gr.Number(label="sum")
    def add(num1, num2):
        return num1 + num2
    add_btn.click(add, inputs=[a, b], outputs=c)
    def sub(data):
        # 这里的a和b不是索引下标，而是表示创建的gradio组件
        # inputs={a, b} 使用 {} 表示传给 gr 的是一个组件集合，而使用 [a,b] 表示传给gr的是具体的数据
        # inputs={a,b} 被接收后解析为 data={a: 3, b: 5}，因此取key=a即可得到key=a对应的value=3
        return data[a] - data[b]
    sub_btn.click(sub, inputs={a, b}, outputs=c)
# demo2.launch()



import gradio as gr

def change_textbox(choice):
    if choice == "short":
        return gr.Textbox(lines=2, visible=True)
    elif choice == "long":
        return gr.Textbox(lines=8, visible=True, value="Lorem ipsum dolor sit amet")
    else:
        return gr.Textbox(visible=False)

with gr.Blocks() as demo:
    radio = gr.Radio(
        ["short", "long", "none"], label="What kind of essay would you like to write?"
    )
    text = gr.Textbox(lines=2, interactive=True, buttons=["copy"])
    radio.change(fn=change_textbox, inputs=radio, outputs=text)

demo.launch()




