class Paddle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [0, 0]  # Paddle's position on the screen

    def move(self, x, y):
        """Move the paddle to a new position."""
        self.position[0] += x
        self.position[1] += y

    def get_position(self):
        """Return the current position of the paddle."""
        return self.position

    def reset_position(self, screen_width):
        """Reset the paddle's position to the center of the screen."""
        self.position[0] = (screen_width - self.width) / 2
        self.position[1] = 0  # Reset to the bottom of the screen