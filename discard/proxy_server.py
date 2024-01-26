from flask import Flask, request, make_response, Response
import requests
import FakeGLM.discard.get_token as get_token

app = Flask(__name__)

# 假设这是智谱大模型的API端点
ZHIPU_API_ENDPOINT = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

@app.route('/v1/chat/completions', methods=['POST'])
def predict():
    # 获取fastgpt的原始请求数据
    data = request.json
    print(data)
    Authorization=request.headers.get('Authorization').split(" ")[-1]
    # 检查并删除或修改top_p参数
    if 'top_p' in data and (data['top_p'] == 0 or data['top_p'] == 1):
        del data['top_p']  # 或者根据需要设置一个合法的值
    Bearer=get_token.generate_token(Authorization, 600000)
    headers={"Authorization":Bearer}
    # 转发给智谱大模型，并启用流式传输
    response = requests.post(ZHIPU_API_ENDPOINT, json=data, headers=headers, stream=True)
    # 创建一个生成器函数来逐块读取智谱大模型的流式响应
    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk
    
    # 返回一个流式响应给fastgpt
    return Response(generate(), content_type=response.headers.get('Content-Type'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
