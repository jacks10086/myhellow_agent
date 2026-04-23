"""

配置类
"""

import os

class Config:
    model_id: str = os.getenv("LLM_MODEL_ID")
    base_url: str = os.getenv("LLM_BASE_URL")
    api_key: str = os.getenv("LLM_API_KEY")
    temperature: float = 0.7
