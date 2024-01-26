import base64
from PIL import Image
from io import BytesIO
import imghdr

def resize_image_if_needed(base64_str):
    # 解码base64字符串
    image_data = base64.b64decode(base64_str)
    # 尝试检测图片类型
    image_extension = imghdr.what(None, h=image_data)
    # 如果无法检测到图片类型，可以默认保存为JPG
    if not image_extension:
        image_extension = 'jpg'
    # 使用BytesIO创建一个字节流
    image = Image.open(BytesIO(image_data))
    # 获取图像的尺寸
    width, height = image.size
    # 判断最长边是否大于1024
    if max(width, height) > 1024:
        # 计算缩放比例
        scale = 1024 / max(width, height)
        # 新的尺寸
        new_size = (int(width * scale), int(height * scale))
        # 缩放图像
        image = image.resize(new_size, Image.LANCZOS)
        # 将缩放后的图像保存到字节流
        temp_byte_io = BytesIO()
        image.save(temp_byte_io, format=image_extension)  # 这里以JPG格式为例，可以根据需要更改
        # 读取字节流中的数据
        temp_byte_io.seek(0)
        resized_image_data = temp_byte_io.read()
        # 对缩放后的图像数据进行base64编码
        resized_base64_str = base64.b64encode(resized_image_data).decode('utf-8')
        return resized_base64_str
    else:
        return base64_str

if __name__=="__main__":
    # 示例使用
    base64_str = "你的base64编码字符串"
    resized_base64_str = resize_image_if_needed(base64_str)
    print(resized_base64_str)
