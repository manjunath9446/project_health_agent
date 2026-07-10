from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import AsyncGroq
from loguru import logger

# Load .env from project root
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

class LLMService:

    def __init__(self):

        # Only load .env locally if it exists
        if ENV_PATH.exists():
            load_dotenv(dotenv_path=ENV_PATH)

        api_key = os.environ.get("GROQ_API_KEY")

        logger.info("Running Environment : {}", os.getenv("RENDER", "LOCAL"))
        logger.info("Using .env file     : {}", ENV_PATH.exists())
        logger.info("API Key Available   : {}", "YES" if api_key else "NO")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY environment variable not found."
            )

        self.client = AsyncGroq(
            api_key=api_key,
        )

        self.default_model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    # =====================================================
    # Chat
    # =====================================================

    async def generate(

        self,

        prompt: str,

        system_prompt: Optional[str] = None,

        temperature: float = 0.2,

        max_tokens: int = 2048,

    ) -> str:

        logger.info(
            "Calling Groq model {}",
            self.default_model,
        )

        messages: List[Dict[str, str]] = []

        if system_prompt:

            messages.append(

                {

                    "role": "system",

                    "content": system_prompt,

                }

            )

        messages.append(

            {

                "role": "user",

                "content": prompt,

            }

        )

        response = await self.client.chat.completions.create(

            model=self.default_model,

            messages=messages,

            temperature=temperature,

            max_completion_tokens=max_tokens,

        )

        return response.choices[0].message.content.strip()

    # =====================================================
    # JSON Generation
    # =====================================================

    async def generate_json(

        self,

        prompt: str,

        system_prompt: Optional[str] = None,

        temperature: float = 0.1,

    ) -> Dict[str, Any]:

        response = await self.generate(

            prompt=prompt,

            system_prompt=system_prompt,

            temperature=temperature,

        )

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            logger.warning(
                "LLM returned non-JSON output."
            )

            return {

                "success": False,

                "raw_response": response,

            }

    # =====================================================
    # Retry Wrapper
    # =====================================================

    async def safe_generate(

        self,

        prompt: str,

        system_prompt: Optional[str] = None,

        retries: int = 3,

    ) -> str:

        last_error = None

        for attempt in range(

            1,

            retries + 1,

        ):

            try:

                return await self.generate(

                    prompt=prompt,

                    system_prompt=system_prompt,

                )

            except Exception as exc:

                last_error = exc

                logger.warning(

                    "Groq attempt {} failed: {}",

                    attempt,

                    exc,

                )

        logger.exception(last_error)

        raise RuntimeError(

            "Groq generation failed after retries."

        )

    # =====================================================
    # Health Check
    # =====================================================

    async def health_check(

        self,

    ) -> bool:

        try:

            reply = await self.generate(

                prompt="Reply with OK.",

                temperature=0,

                max_tokens=10,

            )

            return "OK" in reply.upper()

        except Exception as exc:

            logger.error(

                "Groq health check failed: {}",

                exc,

            )

            return False

    # =====================================================
    # Available Models
    # =====================================================

    @staticmethod
    def supported_models():

        return [

            "llama-3.3-70b-versatile",

            "llama-3.1-8b-instant",

            "meta-llama/llama-4-scout-17b-16e-instruct",

            "meta-llama/llama-4-maverick-17b-128e-instruct",

            "qwen/qwen3-32b",

            "deepseek-r1-distill-llama-70b",

        ]

    # =====================================================
    # Debug
    # =====================================================

    async def test(

        self,

    ):

        response = await self.generate(

            prompt="Introduce yourself in one sentence."

        )

        print()

        print("=" * 80)

        print("LLM TEST")

        print("=" * 80)

        print(response)

        print()

        print("=" * 80)