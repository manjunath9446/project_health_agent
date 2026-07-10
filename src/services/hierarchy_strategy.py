from __future__ import annotations

from typing import Dict, List


class HierarchyStrategy:
    """
    Determines depth for every task.

    Supports:

    Parent ID
    WBS
    Level
    Ancestors
    Flat
    """

    def apply(
        self,
        rows: List[Dict],
        hierarchy_type: str,
    ) -> List[Dict]:

        if hierarchy_type == "parent_id":
            return self._parent(rows)

        if hierarchy_type == "wbs":
            return self._wbs(rows)

        if hierarchy_type == "level":
            return self._level(rows)

        if hierarchy_type == "ancestors":
            return self._ancestors(rows)

        return self._flat(rows)

    # -----------------------------------------------------

    def _level(self, rows):

        for row in rows:

            level = row.get("level")

            try:
                row["_depth"] = int(level)

            except Exception:
                row["_depth"] = 1

        return rows

    # -----------------------------------------------------

    def _ancestors(self, rows):

        

        for i, row in enumerate(rows[:20]):

            print(
                i,
                row.get("task_name"),
                row.get("ancestors"),
            )

        for row in rows:

            level = row.get("ancestors")

            try:
                row["_depth"] = int(level) + 1
            except Exception:
                row["_depth"] = 1

        return rows

    # -----------------------------------------------------

    def _wbs(self, rows):

        for row in rows:

            wbs = row.get("wbs")

            if wbs is None:
                row["_depth"] = 1
                continue

            row["_depth"] = len(str(wbs).split("."))

        return rows

    # -----------------------------------------------------

    def _parent(self, rows):

        lookup = {}

        for i, row in enumerate(rows):
            lookup[row.get("id", i)] = row

        for row in rows:

            parent = row.get("parent_id")

            if parent is None:
                row["_depth"] = 1
                continue

            depth = 2

            current = lookup.get(parent)

            while current:

                depth += 1

                pid = current.get("parent_id")

                if pid is None:
                    break

                current = lookup.get(pid)

            row["_depth"] = depth

        return rows

    # -----------------------------------------------------

    def _flat(self, rows):

        for row in rows:
            row["_depth"] = 1

        return rows