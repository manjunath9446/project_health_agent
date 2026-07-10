from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# ============================================================
# Memory Record
# ============================================================

@dataclass
class MemoryRecord:

    timestamp: datetime

    source: str

    category: str

    content: str

    metadata: Dict = field(default_factory=dict)


# ============================================================
# Memory Service
# ============================================================

class MemoryService:
    """
    Long-term memory for AI agents.

    Stores

        Conversations

        Decisions

        Risks

        Recommendations

        Simulations

        Executive summaries

    """

    def __init__(self):

        self._memory: List[MemoryRecord] = []

    # =====================================================
    # Add Memory
    # =====================================================

    def add(

        self,

        source: str,

        category: str,

        content: str,

        metadata: Optional[Dict] = None,

    ):

        if metadata is None:

            metadata = {}

        self._memory.append(

            MemoryRecord(

                timestamp=datetime.utcnow(),

                source=source,

                category=category,

                content=content,

                metadata=metadata,

            )

        )

    # =====================================================
    # Recent Memory
    # =====================================================

    def recent(

        self,

        limit: int = 10,

    ) -> List[MemoryRecord]:

        return self._memory[-limit:]

    # =====================================================
    # Category Search
    # =====================================================

    def by_category(

        self,

        category: str,

    ) -> List[MemoryRecord]:

        return [

            item

            for item in self._memory

            if item.category.lower()

            == category.lower()

        ]

    # =====================================================
    # Keyword Search
    # =====================================================

    def search(

        self,

        keyword: str,

    ) -> List[MemoryRecord]:

        keyword = keyword.lower()

        return [

            item

            for item in self._memory

            if keyword in item.content.lower()

        ]
        # =====================================================
    # Context Builder
    # =====================================================

    def build_context(

        self,

        limit: int = 15,

    ) -> str:

        records = self.recent(limit)

        context = []

        for record in records:

            context.append(

                f"[{record.timestamp}] "

                f"[{record.category}] "

                f"{record.content}"

            )

        return "\n".join(context)

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self._memory.clear()

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        categories = {}

        for item in self._memory:

            categories.setdefault(

                item.category,

                0,

            )

            categories[item.category] += 1

        return {

            "total": len(self._memory),

            "categories": categories,

        }

    # =====================================================
    # Debug
    # =====================================================

    def print_memory(self):

        print()

        print("=" * 80)

        print("AI MEMORY")

        print("=" * 80)

        for item in self._memory:

            print()

            print(item.timestamp)

            print(item.source)

            print(item.category)

            print(item.content)

        print()

        print("=" * 80)