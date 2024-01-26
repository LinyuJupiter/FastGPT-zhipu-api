import base64
from io import BytesIO
from PIL import Image
# import imghdr


def Generate_images(queue):
    params = queue.get()  # 从队列中获取参数
    base64_image_str=params["base64_image_str"]
    timestamp=params["timestamp"]
    # 移除URL编码的数据URI scheme（如果存在）
    if "data:image" in base64_image_str and ";base64," in base64_image_str:
        header, base64_image_str = base64_image_str.split(";base64,")
    # 去除base64字符串前后的空格
    base64_image_str = base64_image_str.strip()
    # base64字符串解码
    image_data = base64.b64decode(base64_image_str)
    # 使用BytesIO创建一个字节流
    image = Image.open(BytesIO(image_data))
    # # 尝试检测图片类型
    # image_extension = imghdr.what(None, h=image_data)
    # # 如果无法检测到图片类型，可以默认保存为PNG
    # if not image_extension:
    #     image_extension = 'png'
    # 保存图片
    file_path = f"/www/wwwroot/fastgpt/picture/{timestamp}.png"
    image.save(file_path)
