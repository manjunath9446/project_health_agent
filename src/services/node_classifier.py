from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.services.hierarchy_builder import HierarchyNode


@dataclass
class ClassifiedNode:

    node: HierarchyNode

    node_type: str

    children: List["ClassifiedNode"]


class NodeClassifier:
    """
    Enterprise hierarchy classifier.

    Does NOT assume

        depth1=phase

    Instead

        root = project

        depth2 = phase

        depth3 = milestone

        depth>=4 = task

    Can later be template specific.
    """

    def classify(
        self,
        roots: List[HierarchyNode],
    ) -> List[ClassifiedNode]:

        return [
            self._classify(root)
            for root in roots
        ]

    # ----------------------------------------------------

    def _classify(
        self,
        node: HierarchyNode,
    ) -> ClassifiedNode:

        depth = node.depth

        if depth == 1:

            node_type = "project"

        elif depth == 2:

            node_type = "phase"

        elif depth == 3:

            node_type = "milestone"

        else:

            node_type = "task"

        return ClassifiedNode(

            node=node,

            node_type=node_type,

            children=[
                self._classify(c)
                for c in node.children
            ],
        )