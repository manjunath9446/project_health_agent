from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from loguru import logger

from src.services.ai_runtime_service import ai_runtime


# ============================================================
# Chat Message
# ============================================================

@dataclass
class ChatMessage:

    role: str

    content: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )


# ============================================================
# AI Chat Service
# ============================================================

class AIChatService:

    """
    Enterprise AI Copilot.

    Features

        • Multi-turn conversations

        • Memory

        • QA

        • Executive Questions

        • Root Cause

        • Forecast

        • Simulation
    """

    def __init__(self):

        self.history: List[ChatMessage] = []

    # =====================================================

    async def ask(

        self,

        question: str,

    ) -> str:

        logger.info(

            "User: {}",

            question,

        )

        self.history.append(

            ChatMessage(

                role="user",

                content=question,

            )

        )

        answer = await ai_runtime.ask(

            question

        )

        self.history.append(

            ChatMessage(

                role="assistant",

                content=answer,

            )

        )

        return answer

    # =====================================================

    def clear(self):

        self.history.clear()

    # =====================================================

    def last_messages(

        self,

        limit: int = 10,

    ):

        return self.history[-limit:]

    # =====================================================

    def conversation(self):

        return [

            {

                "role": m.role,

                "content": m.content,

                "time": m.timestamp,

            }

            for m in self.history

        ]

    # =====================================================

    def export_context(self):

        context = []

        for message in self.history:

            context.append(

                f"{message.role.upper()}: "

                f"{message.content}"

            )

        return "\n".join(context)

    # =====================================================

    def print_chat(self):

        print()

        print("=" * 80)

        print("AI CHAT")

        print("=" * 80)

        for message in self.history:

            print()

            print(

                message.role.upper()

            )

            print(

                message.content

            )

        print()

        print("=" * 80)


chat_service = AIChatService()