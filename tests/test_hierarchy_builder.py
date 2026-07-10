import pytest
from src.services.hierarchy_builder import HierarchyBuilder
import pandas as pd

def test_build_three_level_tree():
    rows = [
        {"Ancestor Level 1": "Phase1"},
        {"Ancestor Level 1": "Phase1", "Ancestor Level 2": "M1"},
        {"Ancestor Level 1": "Phase1", "Ancestor Level 2": "M1", "Ancestor Level 3": "Task1"},
        {"Ancestor Level 1": "Phase1", "Ancestor Level 2": "M2"},
        {"Ancestor Level 1": "Phase2"},
    ]
    builder = HierarchyBuilder()
    phases = builder.build_tree(rows)
    assert len(phases) == 2
    assert phases[0].name == "Phase1"
    assert len(phases[0].children) == 2  # two milestones
    assert phases[0].children[0].name == "M1"
    assert len(phases[0].children[0].children) == 1
    assert phases[0].children[0].children[0].name == "Task1"