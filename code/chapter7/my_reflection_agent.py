# my_reflection_agent.py
from typing import Optional, Dict
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config

class MyReflectionAgent(ReflectionAgent):
    """
    自定义 Reflection Agent
    展示如何基于框架 ReflectionAgent 基类构建自定义反思迭代智能体
    支持通过 custom_prompts 自定义初始/反思/优化三阶段提示词
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_iterations: int = 3,
        tool_registry=None,
        enable_tool_calling: bool = True,
        custom_prompts: Optional[Dict[str, str]] = None
    ):
        """
        custom_prompts 支持三个 key：
          - "initial":  初始执行提示，模板变量 {task}
          - "reflect":  反思提示，模板变量 {task}, {content}
          - "refine":   优化提示，模板变量 {task}, {feedback}
        """
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            max_iterations=max_iterations,
            tool_registry=tool_registry,
            enable_tool_calling=enable_tool_calling
        )
        self.custom_prompts = custom_prompts or {}
        print(f"✅ {name} 初始化完成，最大迭代: {max_iterations}")

    def _execute_task(self, task: str, **kwargs) -> str:
        if "initial" in self.custom_prompts:
            user_content = self.custom_prompts["initial"].format(task=task)
        else:
            user_content = f"请完成以下任务：\n\n{task}"
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]
        return self._get_llm_response(messages, **kwargs)

    def _reflect_on_result(self, task: str, result: str, **kwargs) -> str:
        if "reflect" in self.custom_prompts:
            user_content = self.custom_prompts["reflect"].format(task=task, content=result)
        else:
            user_content = f"""请仔细审查以下回答，并找出可能的问题或改进空间：

# 原始任务:
{task}

# 当前回答:
{result}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]
        return self._get_llm_response(messages, **kwargs)

    def _refine_result(self, task: str, last_attempt: str, feedback: str, **kwargs) -> str:
        if "refine" in self.custom_prompts:
            user_content = self.custom_prompts["refine"].format(task=task, feedback=feedback)
        else:
            user_content = f"""请根据反馈意见改进你的回答：

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]
        return self._get_llm_response(messages, **kwargs)

    def get_history(self):
        """返回对话历史列表"""
        return self._history
