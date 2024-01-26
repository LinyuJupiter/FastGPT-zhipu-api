from datetime import datetime
import json
import Generate_images
import resize_img
import time
import multiprocessing


def process_request_data(data, ip):
    """
    处理请求数据，修改或删除某些字段。
    对于图像，本方法会将图像存在本地并将URL发送给模型
    """
    # 若top_p值不合理则移除
    if 0<=data.get('top_p')<=1:
        data.pop('top_p', None)
    isPicture = False # 只能有一张图片，仅保留最后一张图片，之前的图片将会被删除，picture_index用来记录上一张图片的位置
    # 创建队列
    queue = multiprocessing.Queue()
    # 创建进程等待保存图片
    p = multiprocessing.Process(target=Generate_images.Generate_images, args=(queue,))
    for i in range(len(data.get('messages'))-1, -1, -1): # 从后往前逐个检查是否有图片
        if data.get('model')=='glm-4v' and data.get('messages')[i]['role']=='user' and type(data.get('messages')[i]['content'])==list:
            if data.get('messages')[i]['content'][0]['type']=='image_url':
                base64_image_str=data.get('messages')[i]['content'][0]['image_url']['url']
                index=0
            else:
                base64_image_str=data.get('messages')[i]['content'][1]['image_url']['url']
                index=1  
            
            if len(data.get('messages')[i]['content'])==1 and index==0: # 只发图片的情况，手动加上文字
                text={"type": "text", "text": "请看这张图片"}
                data['messages'][i]['content'].append(text)

            if isPicture: # 检查之前是否已经有图片
                del data['messages'][i]['content'][index]
            else: # 没有则存图
                isPicture = True
                # 获取时间戳
                timestamp=str(time.time()).replace('.', '')
                url= f"http://{ip}/picture/{timestamp}.png"
                data['messages'][i]['content'][index]['image_url']['url']=url
                # 动态设置参数
                params = {'base64_image_str': base64_image_str, 'timestamp': timestamp}
                # 将参数放入队列
                queue.put(params)
                p.start()
    if p.is_alive():            
        p.join()
    # 获取当前时间
    current_time = datetime.now()
    # 格式化时间字符串
    formatted_time = current_time.strftime("%Y.%m.%d-%H:%M:%S : ")
    print(formatted_time, json.dumps(data, ensure_ascii=False).replace("'",'"'))
    return data


def process_request_data2(data):
    """
    处理请求数据，修改或删除某些字段。
    对于图像，本方法会将图像直接发送给模型，对于过大的图片会强行缩放
    本函数已弃用
    """
    # 若top_p值不合理则移除
    if 0<=data.get('top_p')<=1:
        data.pop('top_p', None)
    picture_index=-1 # 只能有一张图片，仅保留最后一张图片，之前的图片将会被删除，picture_index用来记录上一张图片的位置
    last_index=0
    for i in range(len(data.get('messages'))): # 逐个检查是否有图片
        if data.get('model')=='glm-4v' and data.get('messages')[i]['role']=='user' and type(data.get('messages')[i]['content'])==list:
            if data.get('messages')[i]['content'][0]['type']=='image_url':
                base64_image_str=data.get('messages')[i]['content'][0]['image_url']['url']
                index=0
            else:
                base64_image_str=data.get('messages')[i]['content'][1]['image_url']['url']
                index=1
            _, url=base64_image_str.split(";base64,") # 把base64图片的头部去掉
            
            url=resize_img.resize_image_if_needed(url)

            data['messages'][i]['content'][index]['image_url']['url']=url
            
            if len(data.get('messages')[i]['content'])==1 and index==0: # 只发图片的情况，手动加上文字
                text={"type": "text", "text": "请看这张图片"}
                data['messages'][i]['content'].append(text)

            if picture_index>-1: # 检查之前是否已经有图片
                del data['messages'][picture_index]['content'][last_index]
            picture_index = i
            last_index=index
    # 获取当前时间
    current_time = datetime.now()
    # 格式化时间字符串
    formatted_time = current_time.strftime("%Y.%m.%d-%H:%M:%S : ")
    print(formatted_time, json.dumps(data, ensure_ascii=False).replace("'",'"'))
    return data