"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Current version: the player controls casting with a key press (Task 3),
there are several fish types (Task 2), and each round lasts 30 seconds
(Task 4). When time runs out the round ends and a new one can be started.
"""

import math

from game.hook import Hook, IDLE
from game.fish import create_fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30.0


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: score, timer, hook and fish all reset."""
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            create_fish("minnow", x=100, y=160, direction=1),
            create_fish("minnow", x=500, y=200, direction=-1),
            create_fish("bass",   x=400, y=260, direction=-1),
            create_fish("bass",   x=200, y=320, direction=1),
            create_fish("golden", x=250, y=380, direction=1),
            create_fish("golden", x=600, y=420, direction=-1),
        ]
        self.hooked_fish = None
        self.score = 0
        self.time_left = ROUND_SECONDS
        self.game_over = False

    def cast(self):
        """Player pressed the cast key. Starts a cast only if the hook is
        idle and the round is still running; otherwise ignored."""
        if not self.game_over and self.hook.state == IDLE:
            self.hook.start_cast()

    def update(self, dt):
        """Advance one frame. dt is the elapsed time in seconds."""
        if self.game_over:
            return

        self.time_left -= dt
        if self.time_left <= 0:
            # Round over: freeze everything. A fish that is still on the
            # line (not yet back at the surface) is not scored.
            self.time_left = 0
            self.game_over = True
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                # Award the caught fish's own point value
                self.score += self.hooked_fish.point_value
                self._respawn(self.hooked_fish)
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def _respawn(self, old_fish):
        """Replace a scored fish with a new one of the same type/depth,
        entering from the edge it was heading away from."""
        direction = 1 if old_fish.speed > 0 else -1
        start_x = -old_fish.width if direction == 1 else WIDTH
        self.fish_list.append(
            create_fish(old_fish.fish_type, x=start_x, y=old_fish.home_y, direction=direction)
        )

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {math.ceil(self.time_left)}", (WIDTH - 120, 10))

        if self.game_over:
            renderer.draw_overlay(surface)
            renderer.draw_banner(surface, font, "TIME'S UP!", y_offset=-40)
            renderer.draw_banner(surface, font, f"Final score: {self.score}")
            renderer.draw_banner(surface, font, "Press R to play again", y_offset=40)
        elif self.hook.state == IDLE:
            renderer.draw_text(surface, font, "Press SPACE to cast", (10, HEIGHT - 30))