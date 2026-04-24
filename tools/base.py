"""
基础工具类，定义什么是工具，以及工具的属性和方法。

"""

from typing import Any, List, Optional
from pydantic import BaseModel
from abc import ABC,abstractmethod

class ToolParameter(BaseModel):
    """
    工具参数类，定义工具的参数。
    """
    name:str
    type:str
    description:str
    required:bool = True
    default:Optional[any] = None


class Tool(ABC):
    """
    工具类，定义工具的基本属性和方法。
    抽象方法：run, get_parameters
    """
    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters:dict[str,Any])->str:
        """
        工具运行方法，根据输入消息返回输出消息。
        """
        pass

    @abstractmethod
    def get_parameters(self)->List[ToolParameter]:
        """
        获取工具的参数。
        """
        pass

    def validate_parameters(self, parameters:dict[str,Any])->bool:
        """
        验证工具的必填参数是否符合要求。
        """
        # 检查必填参数是否提供
        required_parameters = [param.name for param in self.get_parameters() if param.required]
        return all(param in parameters for param in required_parameters)

    def to_dict(self)->dict[str,Any]:
        """
        将工具的参数转换为字典。
        """
        return {
            "name":self.name,
            "description":self.description,
            "parameters":[param.model_dump() for param in self.get_parameters()]
        }
