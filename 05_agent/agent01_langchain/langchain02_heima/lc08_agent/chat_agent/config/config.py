#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author    : LuoXianchao
# Datetime  : 2026/5/14 21:09
# Module    : config.py
# explain   : 读取 yaml 配置文件

# 读取 yaml 配置文件
# uv add pyyaml
import yaml

from dataclasses import dataclass

@dataclass
class AppConfig:
    version: str

@dataclass
class LogConfig:
    level: str
    path: str

@dataclass
class AgentConfig:
    external_data_path: str

@dataclass
class PromptConfig:
    main_path: str
    rag_summarize_path: str
    report_path: str

@dataclass
class RagConfig:
    chat_model_name: str
    embedding_model_name: str

@dataclass
class ChromadbConfig:
    path: str

@dataclass
class Config:
    app: AppConfig
    log: LogConfig
    agent: AgentConfig
    prompt: PromptConfig
    rag: RagConfig
    chromadb: ChromadbConfig


from langchain02_heima.lc08_agent.chat_agent.utils.path_tool import get_abs_path

def _read_config() -> Config:
    with open(get_abs_path("config\\config.yml"), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        config = Config(
            app=AppConfig(**data["app"]),
            log=LogConfig(**data["log"]),
            agent=AgentConfig(**data["agent"]),
            prompt=PromptConfig(**data["prompt"]),
            rag=RagConfig(**data["rag"]),
            chromadb=ChromadbConfig(**data["chromadb"]),
        )
        # print('config read file')
        return config

cfg = _read_config()

if __name__ == '__main__':
    print(cfg.app.version)
    print(cfg.log.level)
    print(cfg.log.path)


