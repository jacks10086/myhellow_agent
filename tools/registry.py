"""
工具注册器
"""
from typing import Any, Callable
from base import Tool

class ToolRegistry:
    def __init__(self):
        self._tools:dict[str,Tool] = {}
        self._functions:dict[str,dict[str,Any]] = {}
    #注册方法
    def register_tool(self, tool:Tool):
        """
        注册工具
        """
        if tool.name in self._tools:
            print(f"工具 {tool.name} 已存在，将被覆盖")
        self._tools[tool.name] = tool
        print(f"工具 {tool.name} 注册成功")

    def register_function(self, name:str, desc:str, func:Callable[[str],str]):
        """
        注册函数
         Args:
            name: 工具名称
            desc: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果。目前只满足 参数:str，返回值:str的函数
        """
        if name in self._functions:
            print(f"工具 {name} 已存在，将被覆盖")

        self._functions[name] = {
            "description":desc,
            "func":func
        }
        print(f"工具 {name} 注册成功")
        
    def unregister(self, name:str):
        """
        注销工具
        """
        if name in self._tools:
            del self._tools[name]   
            print(f"工具 {name} 注销成功")
        
        elif name in self._functions:
            del self._functions[name]   
            print(f"工具 {name} 注销成功")

        else:
            print(f"工具 '{name}'不存在")

    def get_tool(self, name:str) -> Optional[Tool]:
        """
        获取工具
        """
        return self._tools.get(name)

    def get_function(self, name:str) -> Optional[Callable]:
        """
        获取函数
        """
        func_info = self._functions.get(name)
        if func_info is None:
            return None
        return func_info["func"]

    def execute_tool(self, name:str, input:str) -> str:
        """
        执行工具
        """
        if  name in self._tools:
            tool = self._tools[name]
            try:
                return tool.run({"input":input})
            except Exception as e:
                raise f"错误：执行工具 {name} 发生异常：{str(e)}"
        
        elif name in self._functions:
            func = self._functions[name]["func"]
            try:
                return func(input)
            except Exception as e:
                raise f"错误：执行函数 {name} 发生异常：{str(e)}"
        else:
            raise ValueError(f"函数 '{name}' 不存在")

    def get_tools_descriptions(self) -> list[str]:
        """
        获取所有工具的描述
        """
        descriptions = []
        # Tool工具对象描述
        for tool in self._tools.values():
            descriptions.append(f"-{tool.name}:{tool.description}")
        
        # 函数工具描述
        for func_name, func_info in self._functions.items():
            descriptions.append(f"-{func_name}:{func_info['description']}")
        
        return "\n".join(descriptions) if descriptions else "暂无可用工具"

    def list_tools(self)->list[str]:
        """
        列出所有工具名称
        """
        return list(self._tools.keys()) + list(self._functions.keys())

    def get_all_tools(self)->list[Tool]:
        """
        获取所有Tool工具对象
        """
        return list(self._tools.values())

    def clear(self):
        """
        清空所有工具
        """
        self._tools.clear()
        self._functions.clear()
        print("所有工具已清空")

# 全局工具注册器
tool_registry = ToolRegistry()