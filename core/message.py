
"""
将dict[str,str]转换为Message消息类
便于管理上下文消息
"""
from typing import Literal,Optional,Iterator

MessageRole=  Literal["user", "assistant", "system", "tool"]

class Message:
    role: MessageRole
    content: Optional[str] = None

    def __init__(self, role: MessageRole, content: str):
        self.role = role
        self.content = content
