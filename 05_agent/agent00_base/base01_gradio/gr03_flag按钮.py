

import gradio as gr

def test_flag(i):
    return f"返回数据：{i}"


# flagging_dir 会在指定的目录下生成一个dataset的csv文件，用于记录用户输入的数据和输出的结果
# 该功能可以用于问题排查

demo = gr.Interface(
    fn=test_flag,
    inputs=["text"],
    outputs=["text"],
    title="flag按钮测试",
    description="对flag按钮的测试描述",
    flagging_dir="./record",
    api_name="predict"
)

demo.launch()
