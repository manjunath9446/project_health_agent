from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from loguru import logger

from src.core.blackboard import Blackboard
from src.services.llm_service import LLMService


# ============================================================
# Plan Step
# ============================================================

@dataclass
class PlanStep:

    step: int

    title: str

    description: str

    completed: bool = False


# ============================================================
# Execution Plan
# ============================================================

@dataclass
class ExecutionPlan:

    goal: str

    steps: List[PlanStep] = field(
        default_factory=list
    )


# ============================================================
# Planning Agent
# ============================================================

class PlanningAgent:

    """
    Converts user goals into execution plans.

    Example

    User:
        Improve project health

    Output:

        1 Recover delayed tasks

        2 Resolve critical risks

        3 Review dependencies

        4 Reforecast schedule
    """

    def __init__(

        self,

        blackboard: Blackboard,

        llm: LLMService,

    ):

        self.blackboard = blackboard

        self.llm = llm

    # =====================================================

    async def create_plan(

        self,

        goal: str,

    ) -> ExecutionPlan:

        logger.info(

            "Planning goal: {}",

            goal,

        )

        health = self.blackboard.get(

            "health_score"

        )

        risk = self.blackboard.get(

            "risk_report"

        )

        recommendation = self.blackboard.get(

            "recommendations"

        )

        prompt = f"""
You are a Senior PMO Director.

Create a step-by-step execution plan.

Goal

{goal}

Health Score

{health.overall_score}

Critical Risks

{risk.critical}

High Risks

{risk.high}

Recommendations

"""

        for rec in recommendation.recommendations:

            prompt += f"""

- {rec.title}

"""

        prompt += """

Return JSON

{
  "steps":[
      {
         "title":"",
         "description":""
      }
  ]
}

Only return JSON.
"""

        response = await self.llm.generate_json(

            prompt

        )

        plan = ExecutionPlan(

            goal=goal

        )

        for i, item in enumerate(

            response.get(

                "steps",

                []

            ),

            start=1,

        ):

            plan.steps.append(

                PlanStep(

                    step=i,

                    title=item.get(

                        "title",

                        ""

                    ),

                    description=item.get(

                        "description",

                        ""

                    ),

                )

            )

        self.blackboard.put(

            key="execution_plan",

            value=plan,

            producer="PlanningAgent",

        )

        return plan

    # =====================================================

    @staticmethod
    def print_plan(

        plan: ExecutionPlan,

    ):

        print()

        print("=" * 90)

        print(plan.goal)

        print("=" * 90)

        print()

        for step in plan.steps:

            print(

                f"{step.step}. {step.title}"

            )

            print(

                f"   {step.description}"

            )

            print()