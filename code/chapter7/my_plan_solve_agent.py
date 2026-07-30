# my_plan_solve_agent.py
from typing import Optional
from hello_agents import PlanSolveAgent, HelloAgentsLLM, Config, Message

class MyPlanAndSolveAgent(PlanSolveAgent):
    """
    自定义 Plan-and-Solve Agent
    展示如何基于框架 PlanSolveAgent 基类构建自定义规划执行智能体
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        planner_prompt: Optional[str] = None,
        executor_prompt: Optional[str] = None,
        tool_registry=None,
        enable_tool_calling: bool = True,
        max_tool_iterations: int = 3
    ):
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            planner_prompt=planner_prompt,
            executor_prompt=executor_prompt,
            tool_registry=tool_registry,
            enable_tool_calling=enable_tool_calling,
            max_tool_iterations=max_tool_iterations
        )
        print(f"✅ {name} 初始化完成")

    def run(self, input_text: str, **kwargs) -> str:
        """
        重写 run 方法，在基类逻辑前后添加自定义日志
        """
        print(f"\n🧠 {self.name} 开始规划并执行: {input_text}")
        result = super().run(input_text, **kwargs)
        print(f"\n✅ {self.name} 执行完毕")
        return result

    def get_history(self):
        """返回对话历史列表"""
        return self._history
