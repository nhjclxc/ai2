import gradio as gr

def mul(num1, num2):
    return  "result：", f"{num1} x {num2} = {num1 * num2}"

demo = gr.Interface(
    fn=mul,
    inputs=["slider", gr.Slider(minimum=1, maximum=10, step=2)],
    outputs=["text", "text"],
    api_name="predict"
)

demo.launch()


