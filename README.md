# FastGPT-zhipu-api

<p align="center">
  <a href="./README_en.md">English</a> |
  <a href="./README.md">简体中文</a>
</p>


本项目是一个使用 FastAPI 构建的 HTTP 服务，主要用于将请求转发到智谱大模型的聊天API。

本项目当前用途是对[FastGPT](https://github.com/labring/FastGPT?tab=readme-ov-file)项目所发送的请求内容进行加工后发送给[智谱](https://open.bigmodel.cn/dev/api#overview)接口，并将返回的内容转发给FastGPT。

## 特性

- **修正参数错误**: 通过反向代理的方式，修复FastGPT接入智谱模型时，会出现“  [*top_p*] *参数非法。请检查文档*   ”的报错。
- **修正发图功能**: 修复FastGPT接入智谱模型时，发送图片会报错的问题。注意：需要使用[glm-4v](https://open.bigmodel.cn/dev/api#glm-4v)模型才能发图，且在FastGPT的[config.json](https://github.com/labring/FastGPT/blob/main/projects/app/data/config.json)中要把对应模型的"vision"设置为true。
- **增加图像生成功能**: 提供一个http接口可以调用智谱的[cogview-3](https://open.bigmodel.cn/dev/api#cogview)模型，配合上FastGPT的高级编排中的[http模块](https://doc.fastgpt.in/docs/workflow/modules/http/)，可以实现让模型生成图片的功能。
- **更多功能**: 还在开发中。

## 安装

要运行此项目，您需要安装 Python 3.8 或更高版本。首先克隆此仓库：

```bash
git clone https://github.com/LinYujupiter/FastGPT-zhipu-api.git
cd FastGPT-zhipu-api
```

## 环境配置

### 使用 Conda

如果您使用 Conda，可以按照以下步骤设置和激活虚拟环境：

1. **创建虚拟环境**：

   ```bash
   conda create -n FastGPT-zhipu-api python=3.8
   ```

2. **激活虚拟环境**：

   ```bash
   conda activate FastGPT-zhipu-api
   ```

3. **安装依赖**：

   在激活的虚拟环境中，运行：

   ```bash
   pip install -r requirements.txt
   ```

### 不使用 Conda

如果您不使用 Conda，可以直接使用 pip 安装依赖：

```bash
pip install -r requirements.txt
```

## 运行

在安装了所有依赖之后，您可以通过以下命令启动服务：

```bash
sh begin.sh
```

您可以通过以下命令停止服务：

```bash
sh end.sh
```

您可以通过以下命令清除运行过程中生成的日志，但是清除后的日志无法恢复，请慎重使用：

```bash
sh clean.sh
```

## 使用

启动服务后，您可以通过以下URL使用API：

```
http://localhost:5000/v1/chat/completions # 聊天模型
http://localhost:5000/vv4/images/generations # 图像生成模型
```

### 聊天功能

具体来说，您应该按照FastGPT的官方文档中对于[one-api](https://github.com/songquanpeng/one-api)的[配置说明](https://doc.fastgpt.in/docs/development/one-api/)，先将one-api安装完毕且将FastGPT的[docker-compose.yml](https://github.com/labring/FastGPT/blob/main/files/deploy/fastgpt/docker-compose.yml)配置完成。

然后，在本服务已经运行的基础上，在**one-api**中新建一个自定义渠道，将**Base URL**改为上述聊天模型的URL，并填入*glm-4*、*glm-4v*、*glm-3-turbo*等模型名称，以及智谱的**api-key**。注意，在使用本渠道之后，记得禁用原先设置的智谱渠道。

### 绘图功能

本项目的发图功能是对智谱接口进行重写，对于请求体的字段与接收体的字段都重新定义了。您应该使用FastGPT的高级编排中的**HTTP模块**来开发您的绘图应用。

此处有一个<a href="./example.json">示例</a>，您可以使用FastGPT的高级编排的*导入*功能导入示例配置。您也可以根据自己的需要，使用FastGPT的高级编排功能实现您想要的应用。

## 开发

- **FastAPI**: 用于构建API的主框架。
- **httpx**: 用于异步发送HTTP请求。
- **PyJWT**: 用于生成JWT令牌。

## 贡献

我们欢迎任何形式的贡献，无论是新功能的提议、代码改进还是问题报告。请确保遵循最佳实践和代码风格指南。
