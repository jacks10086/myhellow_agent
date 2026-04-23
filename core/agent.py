"""
智能体基类，在llm基础上搭建智能体基类
v1:需要先区分系统提示词和用户提示词
"""

from core.llm import MyLLM
from abc import ABC,abstractmethod
from typing import Optional
from core.message import Message
from core.config import Config

class BaseAgent(ABC):
    agentName: Optional[str] = None           # 智能体名称
    llm: MyLLM                                # LLM模型
    systemPrompt: Optional[str] = None        # 系统提示词
    _history: list[Message] = []             # 历史记录 私有属性
    config: Optional[Config] = None           # 配置类

    def __init__(
        self, 
        name: str, 
        llm: MyLLM,
        system_prompt: Optional[str] = None,      
        config: Optional[Config] = None
        ):
        self.agentName = name
        self.llm = llm
        self.systemPrompt = system_prompt
        self.config = config or Config()
        self._history = []

    @abstractmethod
    def run(self, input:str, **kwargs) -> str:
        """
        智能体运行方法，根据输入消息返回输出消息
        """
        pass

    def add_message(self, message:Message):
        """
        添加消息到历史记录
        """
        self._history.append(message)

    def get_history(self) -> list[Message]:
        """
        获取历史记录的拷贝,防止修改原始历史记录
        """
        return self._history.copy()

    def clear_history(self):
        """
        清空历史记录
        """
        self._history.clear()