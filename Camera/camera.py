import pygame

class Camera:
    def __init__(self, follow_target, screen_width, screen_height, world_width=2400, world_height=1800):
        self.target = follow_target
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pygame.math.Vector2(0, 0)

    def update(self):
        # Calculate the offset needed to center the camera on the player
        target_x = self.target.position[0] - self.screen_width // 2
        target_y = self.target.position[1] - self.screen_height // 2

        # Clamp the values so the camera does not move outside the world boundaries
        self.offset.x = max(0, min(target_x, self.world_width - self.screen_width))
        self.offset.y = max(0, min(target_y, self.world_height - self.screen_height))

    def apply(self, position):
        # Apply the calculated offset to the given position
        new_position = position[0] - self.offset.x, position[1] - self.offset.y
        return new_position
    