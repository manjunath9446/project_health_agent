from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List, Optional


# ============================================================
# Blackboard Entry
# ============================================================

@dataclass
class BlackboardEntry:

    key: str

    value: Any

    producer: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )


# ============================================================
# Blackboard
# ============================================================

class Blackboard:
    """
    Shared memory for all AI agents.

    Every agent

        READS

    and

        WRITES

    here.

    No agent communicates directly with
    another agent.
    """

    def __init__(self):

        self._memory: Dict[str, BlackboardEntry] = {}

        self._history: List[BlackboardEntry] = []

        self._lock = Lock()

    # ========================================================
    # Write
    # ========================================================

    def put(

        self,

        key: str,

        value: Any,

        producer: str,

    ):

        with self._lock:

            entry = BlackboardEntry(

                key=key,

                value=value,

                producer=producer,
            )

            self._memory[key] = entry

            self._history.append(entry)

    # ========================================================
    # Read
    # ========================================================

    def get(

        self,

        key: str,

        default=None,

    ):

        with self._lock:

            entry = self._memory.get(key)

            if entry is None:

                return default

            return entry.value

    # ========================================================
    # Exists
    # ========================================================

    def exists(

        self,

        key: str,

    ) -> bool:

        return key in self._memory

    # ========================================================
    # Remove
    # ========================================================

    def remove(

        self,

        key: str,

    ):

        with self._lock:

            if key in self._memory:

                del self._memory[key]

    # ========================================================
    # Keys
    # ========================================================

    def keys(

        self,
    ) -> List[str]:

        return list(

            self._memory.keys()

        )

    # ========================================================
    # Snapshot
    # ========================================================

    def snapshot(

        self,
    ) -> Dict[str, Any]:

        return {

            key: value.value

            for key, value

            in self._memory.items()

        }

    # ========================================================
    # History
    # ========================================================

    def history(

        self,

    ) -> List[BlackboardEntry]:

        return list(

            self._history

        )

    # ========================================================
    # Clear
    # ========================================================

    def clear(

        self,

    ):

        with self._lock:

            self._memory.clear()

            self._history.clear()

    # ========================================================
    # Debug
    # ========================================================

    def print_board(

        self,

    ):

        print()

        print("=" * 80)

        print("BLACKBOARD")

        print("=" * 80)

        for key, value in self._memory.items():

            print()

            print(key)

            print(

                "Producer :",

                value.producer,

            )

            print(

                "Time     :",

                value.timestamp,

            )

            print(

                "Type     :",

                type(value.value).__name__,
            )

        print()

        print("=" * 80)