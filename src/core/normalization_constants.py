"""Central place for all value normalisation rules. Update these to change system behaviour."""

# Status normalisation (raw -> canonical)
STATUS_MAP = {
    "completed": "Completed",
    "c": "Completed",
    "in progress": "In Progress",
    "in-progress": "In Progress",
    "ip": "In Progress",
    "not started": "Not Started",
    "ns": "Not Started",
}

# Schedule health normalisation
SCHEDULE_HEALTH_MAP = {
    "green": "Green",
    "yellow": "Yellow",
    "amber": "Yellow",   # treat amber as Yellow
    "red": "Red",
}

# Boolean true values (lowercase)
BOOLEAN_TRUE_VALUES = {"yes", "true", "1", "x", "y", "t"}

# Date formats to try, in order
DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%d-%b-%Y",
    "%b %d, %Y",
]

# Separators for dependency strings
DEPENDENCY_SEPARATORS = r'[;,|\n]+'