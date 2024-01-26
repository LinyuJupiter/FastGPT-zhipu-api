import asyncio
from email import message
import json
import time
import requests
from datetime import datetime
import httpx
import jwt
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import process_request_data

app = FastAPI()

# 配置常量
ZHIPU_API_ENDPOINT = 'https://open.bigmodel.cn/api/paas/v4/chat/completions' # 聊天模型
ZHIPU_API_COGVIEW = 'https://open.bigmodel.cn/api/paas/v4/images/generations' # 绘图模型
TOKEN_EXPIRY = 600000 # 生成10分钟的授权token
IP = 'YOUR_SERVER_IP' # 服务器ip地址


@app.post("/v1/chat/completions")
async def predict(request: Request):
    """
    处理POST请求，转发到智谱大模型，并返回流式响应。
    """
    # 获取请求数据
    data = await request.json()

    # 生成带有认证信息的请求头
    authorization = request.headers.get('Authorization', '').split(" ")[-1]
    headers = {"Authorization": generate_token(authorization, TOKEN_EXPIRY)}

    # 处理请求参数
    data = process_request_data.process_request_data(data, IP)

    # 异步转发请求并获取响应
    async with httpx.AsyncClient() as client:
        response = await client.post(ZHIPU_API_ENDPOINT, json=data, headers=headers)

    # 创建并返回流式响应
    return StreamingResponse(stream_response(response), media_type=response.headers.get('Content-Type'))

@app.post("/v4/images/generations")
async def generate(request: Request):
    """
    处理POST请求，转发到智谱图像大模型，并返回响应。
    """
    try:
        # 获取请求数据
        data = await request.json()
        # 生成带有认证信息的请求头
        authorization = request.headers.get('Authorization', '').split(" ")[-1]
        headers = {"Authorization": generate_token(authorization, TOKEN_EXPIRY)}
        if "model" not in data:
            data["model"]="cogview-3"
        if "data" in data:
            data["prompt"]=data["data"]["prompt"]
            del data["data"]
        # 在线程池中执行同步请求
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.post(ZHIPU_API_COGVIEW, json=data, headers=headers))
        res = response.json()
        # 这里可以根据需要处理响应数据
        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间字符串
        formatted_time = current_time.strftime("%Y.%m.%d-%H:%M:%S : ")
        print(current_time, res)
        # 直接返回字典，FastAPI会自动将其转换为JSON响应
        return res
    except Exception as e:
        # 这里可以根据需要处理错误
        print(f"An error occurred: {e}")
        return {"data": "An error occurred while processing the request."}


async def stream_response(response):
    """
    创建一个异步生成器，用于逐块读取并返回响应内容。
    """
    async for chunk in response.aiter_bytes():
        yield chunk


def generate_token(apikey: str, exp_seconds: int):
    """
    生成带有有效期的JWT令牌。
    """
    try:
        api_key, secret = apikey.split(".")
    except ValueError:
        raise ValueError("无效的apikey格式")

    exp = int(time.time() * 1000) + exp_seconds * 1000
    payload = {
        "api_key": api_key,
        "exp": exp,
        "timestamp": exp - exp_seconds * 1000,
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
