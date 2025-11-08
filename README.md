# MCP Example

[MCP Python-SDK](https://github.com/modelcontextprotocol/python-sdk)

## 环境配置

本项目使用 [uv](https://docs.astral.sh/uv/) 进行依赖管理。直接按照下述方法启动服务器即可自动安装依赖。

## 启动 MCP 服务器

在根目录执行：

```bash
uv run -m server
```

## 运行客户端示例

在根目录执行：

```bash
uv run -m client
```

## 服务器配置

参考 `config.py` 文件，可以修改服务器的地址和端口号。
