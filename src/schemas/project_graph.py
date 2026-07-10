from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GraphNode:
    """
    Generic graph node.

    Represents one business object inside the project.
    """

    id: str

    node_type: str

    name: str

    parent: Optional[str] = None

    children: List[str] = field(default_factory=list)

    properties: Dict = field(default_factory=dict)


@dataclass
class ProjectGraph:
    """
    Entire project represented as a graph.
    """

    project_name: str

    nodes: Dict[str, GraphNode] = field(default_factory=dict)

    root_id: Optional[str] = None

    # ---------------------------------------------

    def add_node(
        self,
        node: GraphNode,
    ):

        self.nodes[node.id] = node

    # ---------------------------------------------

    def get(
        self,
        node_id: str,
    ) -> Optional[GraphNode]:

        return self.nodes.get(node_id)

    # ---------------------------------------------

    def children(
        self,
        node_id: str,
    ) -> List[GraphNode]:

        node = self.get(node_id)

        if node is None:
            return []

        return [
            self.nodes[c]
            for c in node.children
            if c in self.nodes
        ]

    # ---------------------------------------------

    def parents(
        self,
        node_id: str,
    ) -> List[GraphNode]:

        result = []

        current = self.get(node_id)

        while current and current.parent:

            parent = self.get(current.parent)

            if parent is None:
                break

            result.append(parent)

            current = parent

        return result

    # ---------------------------------------------

    def all_nodes(self):

        return list(self.nodes.values())

    # ---------------------------------------------

    def by_type(
        self,
        node_type: str,
    ):

        return [

            n

            for n in self.nodes.values()

            if n.node_type == node_type

        ]

    # ---------------------------------------------

    def statistics(self):

        return {

            "total_nodes": len(self.nodes),

            "projects": len(self.by_type("project")),

            "phases": len(self.by_type("phase")),

            "milestones": len(self.by_type("milestone")),

            "tasks": len(self.by_type("task")),

        }