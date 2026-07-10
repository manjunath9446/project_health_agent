from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HierarchyNode:
    """
    Generic hierarchy node.

    Represents a node in the project hierarchy.
    No assumptions about Phase / Milestone / Task.
    """

    id: int

    name: str

    depth: int

    raw_data: Dict[str, Any]

    parent: Optional["HierarchyNode"] = None

    children: List["HierarchyNode"] = field(default_factory=list)

    sequence: int = 0

    # --------------------------------------------------------

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    # --------------------------------------------------------

    def add_child(
        self,
        child: "HierarchyNode",
    ) -> None:

        child.parent = self
        self.children.append(child)

    # --------------------------------------------------------

    def ancestors(self) -> List["HierarchyNode"]:

        nodes = []

        current = self.parent

        while current:

            nodes.append(current)

            current = current.parent

        nodes.reverse()

        return nodes

    # --------------------------------------------------------

    def descendants(self) -> List["HierarchyNode"]:

        nodes = []

        def dfs(node: "HierarchyNode"):

            for child in node.children:

                nodes.append(child)

                dfs(child)

        dfs(self)

        return nodes

    # --------------------------------------------------------

    def walk(self):

        yield self

        for child in self.children:

            yield from child.walk()


# ============================================================
# Hierarchy Builder
# ============================================================


class HierarchyBuilder:
    """
    Generic hierarchy builder.

    Input
    -----

    [
        {
            "_depth": 1,
            "task_name": "...",
            ...
        }
    ]

    Output
    ------

    List[HierarchyNode]

    Only understands hierarchy depth.
    """

    # --------------------------------------------------------

    def build(
        self,
        rows: List[Dict[str, Any]],
    ) -> List[HierarchyNode]:

        if not rows:
            return []

        roots: List[HierarchyNode] = []

        stack: List[HierarchyNode] = []

        node_id = 1

        for sequence, row in enumerate(rows):

            depth = self._safe_depth(
                row.get("_depth")
            )

            node = HierarchyNode(

                id=node_id,

                name=self._node_name(row),

                depth=depth,

                raw_data=row,

                sequence=sequence,
            )

            node_id += 1

            # --------------------------------------------
            # Move stack to correct parent
            # --------------------------------------------

            while stack and stack[-1].depth >= depth:

                stack.pop()

            # --------------------------------------------

            if not stack:

                roots.append(node)

            else:

                stack[-1].add_child(node)

            stack.append(node)

        return roots

    # ====================================================

    @staticmethod
    def _safe_depth(value) -> int:

        try:

            depth = int(value)

            return max(depth, 1)

        except Exception:

            return 1

    # ====================================================

    @staticmethod
    def _node_name(
        row: Dict[str, Any],
    ) -> str:

        candidates = [

            "task_name",

            "name",

            "activity",

            "activity_name",

            "title",

            "summary",

            "milestone",

            "phase",

        ]

        for field in candidates:

            value = row.get(field)

            if value is None:
                continue

            value = str(value).strip()

            if value:

                return value

        return "Unnamed Node"

    # ====================================================

    @staticmethod
    def flatten(
        roots: List[HierarchyNode],
    ) -> List[HierarchyNode]:

        nodes = []

        def dfs(node: HierarchyNode):

            nodes.append(node)

            for child in node.children:

                dfs(child)

        for root in roots:

            dfs(root)

        return nodes

    # ====================================================

    @staticmethod
    def max_depth(
        roots: List[HierarchyNode],
    ) -> int:

        nodes = HierarchyBuilder.flatten(roots)

        if not nodes:
            return 0

        return max(node.depth for node in nodes)

    # ====================================================

    @staticmethod
    def count_nodes(
        roots: List[HierarchyNode],
    ) -> int:

        return len(
            HierarchyBuilder.flatten(roots)
        )

    # ====================================================

    @staticmethod
    def find_by_name(
        roots: List[HierarchyNode],
        name: str,
    ) -> Optional[HierarchyNode]:

        target = name.strip().lower()

        for node in HierarchyBuilder.flatten(roots):

            if node.name.lower() == target:

                return node

        return None

    # ====================================================

    @staticmethod
    def print_tree(
        roots: List[HierarchyNode],
    ) -> None:

        def dfs(
            node: HierarchyNode,
            indent: int,
        ):

            print(
                "    " * indent
                + f"├── {node.name} (depth={node.depth})"
            )

            for child in node.children:

                dfs(
                    child,
                    indent + 1,
                )

        for root in roots:

            dfs(
                root,
                0,
            )

    # ====================================================

    @staticmethod
    def statistics(
        roots: List[HierarchyNode],
    ) -> Dict[str, int]:

        nodes = HierarchyBuilder.flatten(roots)

        return {

            "root_nodes": len(roots),

            "total_nodes": len(nodes),

            "max_depth": (
                max(n.depth for n in nodes)
                if nodes
                else 0
            ),

            "leaf_nodes": sum(
                1
                for n in nodes
                if n.is_leaf
            ),

            "non_leaf_nodes": sum(
                1
                for n in nodes
                if n.has_children
            ),
        }