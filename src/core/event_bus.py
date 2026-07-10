from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, DefaultDict, Dict, List


# ============================================================
# Event
# ============================================================

@dataclass
class Event:

    name: str

    payload: Dict

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )


# ============================================================
# Event Bus
# ============================================================

class EventBus:
    """
    Event-driven communication layer.

    Agents never call each other directly.

    Instead:

        publish()

    and

        subscribe()
    """

    def __init__(self):

        self._handlers: DefaultDict[
            str,
            List[Callable]
        ] = defaultdict(list)

        self._history: List[Event] = []

    # =====================================================
    # Subscribe
    # =====================================================

    def subscribe(

        self,

        event_name: str,

        handler: Callable,

    ):

        self._handlers[
            event_name
        ].append(handler)

    # =====================================================
    # Publish
    # =====================================================

    def publish(

        self,

        event_name: str,

        payload: Dict | None = None,

    ):

        if payload is None:

            payload = {}

        event = Event(

            name=event_name,

            payload=payload,

        )

        self._history.append(event)

        handlers = self._handlers.get(

            event_name,

            [],

        )

        for handler in handlers:

            handler(event)

    # =====================================================
    # History
    # =====================================================

    def history(

        self,

    ) -> List[Event]:

        return list(

            self._history

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self._history.clear()

        self._handlers.clear()

    # =====================================================
    # Registered Events
    # =====================================================

    def registered_events(self):

        return list(

            self._handlers.keys()

        )

    # =====================================================
    # Debug
    # =====================================================

    def print_history(self):

        print()

        print("=" * 80)

        print("EVENT BUS")

        print("=" * 80)

        for event in self._history:

            print()

            print(

                event.timestamp,

                event.name,

            )

            print(

                event.payload

            )

        print()

        print("=" * 80)
        