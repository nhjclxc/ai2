import random

import gradio as gr
from gradio.themes.builder_app import history

# 1、全局状态

scores = [random.randint(1, 100) for _ in range(10)]
scores.sort(reverse=True)
print(f"学生分数：{scores}")

def topn(n):
    # 获取topn的分数
    return scores[:n].copy()

demo = gr.Interface(
    fn=topn,
    inputs=[gr.Number(label="score")],
    outputs=[gr.JSON()],
    api_name="predict",
)

# demo.launch()


# 2、会话状态

def store_message(msg: str, store: list[str]):
    history = {
        "current": msg,
        "history": store[0:len(store)],
    }
    store.append(msg)
    return history, store


demo2 = gr.Interface(
    fn=store_message,
    inputs=["text", gr.State(value=[])],
    outputs=["json", gr.State()],
    api_name="predict",
)
demo2.launch()



