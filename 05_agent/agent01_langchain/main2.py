from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import openai
from openai import OpenAI
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__) / ".env")

api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_api_key2 = os.environ.get('DEEPSEEK_API_KEY')
print(f"deepseek_api_key: {deepseek_api_key}")
print(f"deepseek_api_key2: {deepseek_api_key2}")
print(deepseek_api_key2 == deepseek_api_key)

key2 = os.getenv("KEY2")
# print(f"api_key: {api_key}")
# print(f"key2: {key2}")

os.environ["HTTP_PROXY"] = "http://127.0.0.1:10808"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"

# base_url = "https://api.zhizengzeng.com/v1/"

def check_openai_api():
    openai.api_key = api_key
    # openai.base_url = base_url
    # resp = requests.get("https://api.openai.com/v1/models")
    # print(resp.status_code)
    # print(resp.text)

    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Write a one-sentence bedtime story about a unicorn."
    )

    print("response:", response.output_text)

def check_langchain_api():

    # 这里是由deepseek的地址来调用，免开代理
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=deepseek_api_key,
        base_url="https://api.deepseek.com"
    )

    # llm.stream()

    # content='你好！很高兴见到你😊 有什么我可以帮你的吗？无论是聊聊天、解答问题，还是需要协助完成某些任务，我都在这里！' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 32, 'prompt_tokens': 5, 'total_tokens': 37, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 5}, 'model_provider': 'openai', 'model_name': 'deepseek-v4-flash', 'system_fingerprint': 'fp_058df29938_prod0820_fp8_kvcache_20260402', 'id': '0f4c256f-a26d-4cfb-9d58-0f934a37e7f6', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019dc85f-934f-74d0-8aaa-5626557fc998-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 5, 'output_tokens': 32, 'total_tokens': 37, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}
    print(llm.invoke("你好"))

    pass

def main():
    print("Hello from agent01-langchain!")
    # check_openai_api()
    # check_langchain_api()



if __name__ == "__main__":
    main()

# uv run .\main.py