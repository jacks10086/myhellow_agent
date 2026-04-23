"""
SimpleAgent 真实测试 - 使用 .env 配置调用实际 LLM API
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from agents.simple_agent import SimpleAgent
from core.llm import MyLLM

load_dotenv()


def test_invoke():
    """测试非流式调用"""
    llm = MyLLM()
    agent = SimpleAgent(
        name="助手",
        llm=llm,
        system_prompt="你是一个友好的助手，请简洁回答问题。"
    )

    print("=" * 50)
    print("测试非流式调用")
    print("=" * 50)

    response = agent.run("你好，请自我介绍")
    print(f"\n回复: {response}")

    # 测试历史记录
    print(f"\n历史记录条数: {len(agent.get_history())}")

    # 第二轮对话
    print("\n" + "=" * 50)
    print("第二轮对话（带历史记录）")
    print("=" * 50)
    response2 = agent.run("我刚才问了什么？")
    print(f"\n回复: {response2}")

    return response, response2


def test_stream():
    """测试流式调用"""
    llm = MyLLM()
    agent = SimpleAgent(
        name="助手",
        llm=llm,
        system_prompt="你是一个友好的助手，请简洁回答问题。"
    )

    print("\n" + "=" * 50)
    print("测试流式调用")
    print("=" * 50)

    print("\n回复: ", end="")
    for chunk in agent.stream_run("用一句话介绍Python"):
        print(chunk, end="", flush=True)
    print()

    return True


if __name__ == "__main__":
    print("开始测试 SimpleAgent...\n")

    # 测试非流式
  #  test_invoke()

    # 测试流式
    test_stream()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
