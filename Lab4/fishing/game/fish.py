"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. Several fish types exist, differing in speed, point
value, size and color.
"""

import pygame

# name -> (speed, point_value, width, height, color)
FISH_TYPES = {
    "minnow": {"speed": 2, "point_value": 10, "width": 36, "height": 18, "color": (80, 180, 220)},   # slow, low value
    "bass":   {"speed": 3, "point_value": 25, "width": 30, "height": 16, "color": (90, 200, 110)},   # medium
    "golden": {"speed": 5, "point_value": 50, "width": 22, "height": 12, "color": (255, 210, 60)},   # fast, high value
}


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10,
                 color=(80, 180, 220), fish_type="minnow"):
        self.x = float(x)
        self.y = y
        self.home_y = y  # swimming depth (y changes while the fish is hooked)
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color
        self.fish_type = fish_type

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )


def create_fish(fish_type, x, y, direction=1):
    """Build a Fish of the given type. direction is 1 (right) or -1 (left)."""
    spec = FISH_TYPES[fish_type]
    return Fish(
        x=x,
        y=y,
        speed=spec["speed"] * direction,
        width=spec["width"],
        height=spec["height"],
        point_value=spec["point_value"],
        color=spec["color"],
        fish_type=fish_type,
    )