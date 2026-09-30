"""
Hook: the player's fishing hook. Moves only vertically, at a fixed
horizontal position. A cast is started by the player (via the engine);
the hook then travels down and returns on its own, and a new cast
cannot interrupt one that is already in progress.
"""

import pygame

IDLE = "idle"
CASTING = "casting"
RETRACTING = "retracting"


class Hook:
    def __init__(self, x, surface_y, max_depth_y, speed=4, width=14, height=14):
        self.x = x
        self.surface_y = surface_y
        self.max_depth_y = max_depth_y
        self.y = surface_y
        self.speed = speed
        self.width = width
        self.height = height
        self.state = IDLE

    def start_cast(self):
        """Begin a cast. Only works when idle; returns True if a cast
        started, False if one is already in progress."""
        if self.state != IDLE:
            return False
        self.state = CASTING
        self.y = self.surface_y
        return True

    def update(self):
        if self.state == CASTING:
            self.y += self.speed
            if self.y >= self.max_depth_y:
                self.y = self.max_depth_y
                self.state = RETRACTING
        elif self.state == RETRACTING:
            self.y -= self.speed
            if self.y <= self.surface_y:
                self.y = self.surface_y
                self.state = IDLE

    def catch_fish(self):
        """Called when a fish has been caught - immediately head back up."""
        self.state = RETRACTING

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )