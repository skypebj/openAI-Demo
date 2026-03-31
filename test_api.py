import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def test():
    try:
        print("正在测试连接...")
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL"),
            messages=[{"role": "user", "content": "你好，测试连接"}]
        )
        print("连接成功！")
        print("返回结果：", response.choices[0].message.content)
    except Exception as e:
        print("连接失败：", e)

if __name__ == "__main__":
    test()
