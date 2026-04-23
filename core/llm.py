"""
LLM
第一版：以openAI的api为基础实现LLM。实现流式和非流式调用。


"""
from openai import OpenAI
import os
from typing import Literal,Optional,Iterator

"""
职责分离，只关心模型调用，不关心其他业务逻辑
#from dotenv import load_dotenv
#load_dotenv()
"""
class MyLLM:
    def __init__(
        self,
        model:Optional[str] = None,
       # provide:Optional[str] = None,
        base_url:Optional[str] = None,
        api_key:Optional[str] = None,
        temperature:float = 0.7,
        **kwargs
    ):    
        self.model = model or os.getenv("LLM_MODEL_ID")
        # self.provide = provide or os.getenv("LLM_PROVIDER")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.temperature = temperature
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            **kwargs
        )
  
    """
    流式调用
    Args:
        message: 消息列表，每个元素是一个字典，包含role和content键值对
        temperature: 温度参数，用于控制模型的输出随机性，默认值为0.7
        kwargs: 其他openAI api支持的参数
    Returns:
        Iterator[str]: 流式的输出，每个元素是一个字符串迭代对象
    """
    def think(self,message:list[dict[str,str]], temperature:Optional[float] = None, **kwargs)->Iterator[str]:
        print(f"正在调用模型{self.model}")
        """
        流式调用
        """

        # 设置温度
        if temperature is not None:
            self.temperature = temperature
       
        # 流式调用
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=message,
                stream=True,
                temperature=self.temperature,
                **kwargs
            )
            # 处理流式响应
            for chunk in response:
                if chunk.choices:  # 检查 choices 是否为空（流式结束时可能为空列表）
                    content = chunk.choices[0].delta.content or ""
                    if content: #最后一个chunk的content为空None，需要过滤
                        print(content, end = "", flush=True)
                        yield content

        except Exception as e:
            print(f"调用模型{self.model}失败，错误信息：{e}")
            raise e

    """
    非流式调用
    Args:
        message: 消息列表，每个元素是一个字典，包含role和content键值对
        temperature: 温度参数，用于控制模型的输出随机性，默认值为0.7
        kwargs: 其他openAI api支持的参数
    Returns:
        str: 模型的输出
       """
    def invoke(self, message:list[dict[str,str]], **kwargs)->str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=message,
                temperature=kwargs.get("temperature", self.temperature),              
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"调用模型{self.model}失败，错误信息：{e}")
            raise e
        
   
