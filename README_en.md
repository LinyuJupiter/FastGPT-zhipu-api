# FastGPT-zhipu-api

<p align="center">
  <a href="./README_en.md">English</a> |
  <a href="./README.md">简体中文</a>
</p>

This project is an HTTP service built using FastAPI, primarily used to forward requests to the chat API of the zhipu Big Model.

The current purpose of this project is to process requests sent by the [FastGPT](https://github.com/labring/FastGPT?tab=readme-ov-file) project, send them to the [zhipu](https://open.bigmodel.cn/dev/api#overview) interface after modification, and forward the returned content to FastGPT.

## Features

- **Correct Parameter Errors**: Fixes the " [*top_p*] *parameter is illegal. Please check the documentation*" error when FastGPT integrates with the zhipu model through reverse proxy.
- **Fix Image Sending**: Resolves the issue of errors when sending images to the zhipu model through FastGPT. Note: The [glm-4v](https://open.bigmodel.cn/dev/api#glm-4v) model must be used for image sending, and the "vision" for the corresponding model in FastGPT's [config.json](https://github.com/labring/FastGPT/blob/main/projects/app/data/config.json) must be set to true.
- **Add Image Generation Function**: Provides an HTTP interface that can call zhipu's [cogview-3](https://open.bigmodel.cn/dev/api#cogview) model. When combined with the [http module](https://doc.fastgpt.in/docs/workflow/modules/http/) in FastGPT's advanced orchestration, it can achieve the functionality of generating images using the model.
- **More Features**: Still in development.

## Installation

To run this project, you need to install Python 3.8 or higher. First, clone this repository:

```bash
git clone https://github.com/LinYujupiter/FastGPT-zhipu-api.git
cd FastGPT-zhipu-api
```

## Environment Configuration

### Using Conda

If you are using Conda, you can set up and activate the virtual environment with the following steps:

1. **Create a virtual environment**:

   ```bash
   conda create -n FastGPT-zhipu-api python=3.8
   ```

2. **Activate the virtual environment**:

   ```bash
   conda activate FastGPT-zhipu-api
   ```

3. **Install dependencies**:

   In the activated virtual environment, run:

   ```bash
   pip install -r requirements.txt
   ```

### Without Conda

If you are not using Conda, you can directly install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running

After installing all dependencies, you can start the service with the following command:

```bash
sh begin.sh
```

You can stop the service with the following command:

```bash
sh end.sh
```

You can clear the logs generated during runtime with the following command. Note that the cleared logs cannot be recovered, so use it with caution:

```bash
sh clean.sh
```

## Usage

After starting the service, you can use the API via the following URLs:

```
http://localhost:5000/v1/chat/completions # Chat model
http://localhost:5000/vv4/images/generations # Image generation model
```

### Chat Functionality

Specifically, you should follow the configuration instructions for [one-api](https://github.com/songquanpeng/one-api) in the official FastGPT documentation for [one-api](https://doc.fastgpt.in/docs/development/one-api/). Install one-api and complete the configuration of FastGPT's [docker-compose.yml](https://github.com/labring/FastGPT/blob/main/files/deploy/fastgpt/docker-compose.yml).

Then, with this service already running, create a custom channel in **one-api**, change the **Base URL** to the URL of the chat model mentioned above, and fill in model names such as *glm-4*, *glm-4v*, *glm-3-turbo*, and the zhipu **api-key**. Note that after using this channel, remember to disable the previously set zhipu channel.

### Drawing Functionality

The image sending functionality of this project is a rewrite of the zhipu interface, defining both the request body and the receiving body fields. You should use the **HTTP module** in FastGPT's advanced orchestration to develop your drawing application.

Here is an [example](./example.json) that you can import using the *Import* feature in FastGPT's advanced orchestration. You can also use the advanced orchestration features of FastGPT to implement the application you desire according to your needs.

## Development

- **FastAPI**: The main framework for building the API.
- **httpx**: Used for asynchronous sending of HTTP requests.
- **PyJWT**: Used to generate JWT tokens.

## Contribution

We welcome contributions in any form, whether it's proposing new features, code improvements, or bug reports. Please make sure to follow best practices and code style guidelines.