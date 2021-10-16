class Vehicle:
    def __init__(self, color: int, size: int, row: int, column: int, direction: int):
        self.color = color
        self.size = size
        self.row = row
        self.column = column

        self.direction = direction


class Node:
    def __init__(self, stage, parent, operator):
        self.stage = stage
        self.parent = parent
        self.operator = operator


class Stage:
    def __init__(self, vehicles, map):
        self.vehicles = vehicles
        self.map = map
