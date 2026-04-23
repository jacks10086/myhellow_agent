"""
简单智能体,实现对话功能
"""

from typing import Optional
from core.agent import BaseAgent
from core.llm import MyLLM
from core.message import Message
from core.config import Config



class SimpleAgent(BaseAgent):
    """
    简单智能体,实现对话功能
    """

    def __init__(
        self,
        name:str,
        llm:MyLLM,
        system_prompt:Optional[str] = None,
        config:Optional[Config] = None
        ):
        super().__init__(name, llm, system_prompt, config)


    def run(self, input:str, **kwargs) -> str:
        """
        智能体非流式运行方法，根据输入消息返回输出消息
        """
        # 检查系统提示词是否为空
        if self.systemPrompt is None:
            self.systemPrompt = ""

        # 构建消息列表
        messages = []

        # 添加系统提示词
        messages.append({"role":"system", "content":self.systemPrompt})
        # 添加历史记录
        for msg in self._history:
            messages.append({"role":msg.role, "content":msg.content})

        # 添加用户提示词
        messages.append({"role":"user", "content":input})

        # 调用llm,非流式调用
        response = self.llm.invoke(messages, **kwargs)

        # 本次会话添加到历史记录
        self.add_message(Message(role="user", content=input))
        self.add_message(Message(role="assistant", content=response))
        
        return response
       
    def stream_run(self, input:str, **kwargs):
        """
        流式调用
        """
        # 检查系统提示词是否为空
        if self.systemPrompt is None:
            self.systemPrompt = ""

        messages = []
        # 添加系统提示词
        messages.append({"role":"system", "content":self.systemPrompt})
        # 添加历史记录
        for msg in self._history:
            messages.append({"role":msg.role, "content":msg.content})

        # 添加用户提示词
        messages.append({"role":"user", "content":input})

        # 调用llm,流式调用
        result = ""
        response = self.llm.think(messages, **kwargs)
        for chunk in response:
            result += chunk
            yield chunk       

        # 添加历史记录
        self.add_message(Message(role="user", content=input))
        self.add_message(Message(role="assistant", content=result))
       
        