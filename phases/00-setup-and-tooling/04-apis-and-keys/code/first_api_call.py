import os
import json
import urllib.request

from openai import OpenAI
import anthropic


def call_deepseek_openai():
    # 1. 从环境变量读取 API Key
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：未设置环境变量 DEEPSEEK_API_KEY")
        print("请在终端中执行: export DEEPSEEK_API_KEY='你的密钥'")
        return

    # 2. 初始化 OpenAI 客户端，指向 DeepSeek 端点
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    # 3. 发送聊天请求
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",  # 或 "deepseek-v4-pro"
            max_tokens=256,
            messages=[
                {"role": "user", "content": "What is a neural network in one sentence?"}
            ]
        )
    except Exception as e:
        print(f"请求失败: {e}")
        return

    # 4. 提取回复内容
    # OpenAI 格式响应为 response.choices[0].message.content
    content = response.choices[0].message.content
    print(f"OpenAI 格式响应: {content}")

    # 5. 打印 token 使用（可选）
    usage = response.usage
    print(f"Tokens used: {usage.prompt_tokens} in, {usage.completion_tokens} out")


def call_deepseek_anthropic():
    # 1. 从环境变量读取 API Key
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：未设置环境变量 DEEPSEEK_API_KEY")
        print("请在终端中执行: export DEEPSEEK_API_KEY='你的密钥'")
        return

    # 2. 初始化 Anthropic 客户端，指向 DeepSeek 的 Anthropic 兼容端点
    client = anthropic.Anthropic(
        base_url="https://api.deepseek.com/anthropic",
        api_key=api_key
    )

    # 3. 发送消息请求
    try:
        response = client.messages.create(
            model="deepseek-v4-flash",  # 或 "deepseek-v4-pro"
            max_tokens=256,
            messages=[
                {"role": "user", "content": "What is a neural network in one sentence?"}
            ]
        )
    except Exception as e:
        print(f"请求失败: {e}")
        return

    # 4. 提取回复内容（处理可能存在的 thinking 块）
    text_parts = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        # 如果是 thinking 块，可以选择忽略或输出
        # elif block.type == "thinking":
        #     print(f"[思考过程] {block.thinking}")
    full_text = " ".join(text_parts) if text_parts else "(无文本回复)"
    print(f"Anthropic 格式响应: {full_text}")

    # 5. 打印 token 使用
    usage = response.usage
    print(f"Tokens used: {usage.input_tokens} in, {usage.output_tokens} out")


def call_raw_http_deepseek():
    # 1. 从环境变量读取 DeepSeek API Key
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：请先设置环境变量 DEEPSEEK_API_KEY")
        print("示例: export DEEPSEEK_API_KEY='sk-你的密钥'")
        return

    # 2. 构造 OpenAI 兼容的请求 URL
    url = "https://api.deepseek.com/chat/completions"

    # 3. 设置请求头（OpenAI 格式）
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # 4. 构造请求体（OpenAI Chat Completion 格式）
    body = json.dumps({
        "model": "deepseek-v4-flash",   # 可改用 "deepseek-v4-pro"
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": "What is a neural network in one sentence?"}
        ]
    }).encode()

    # 5. 发送 POST 请求
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            # 6. 解析 OpenAI 格式的响应
            content = result['choices'][0]['message']['content']
            usage = result['usage']
            print(f"Raw HTTP response: {content}")
            print(f"Tokens used: {usage['prompt_tokens']} in, {usage['completion_tokens']} out")
    except urllib.error.HTTPError as e:
        print(f"HTTP 错误 {e.code}: {e.reason}")
        # 可选：打印服务器返回的详细错误信息
        try:
            error_body = json.loads(e.read())
            print(f"错误详情: {error_body}")
        except:
            pass
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    print("=== API Calls ===\n")
    print("1. Using the SDK:")
    call_deepseek_openai()
    print("\n2. Using the Anthropic SDK:")
    call_deepseek_anthropic()
    print("\n2. Using raw HTTP:")
    call_raw_http_deepseek()
