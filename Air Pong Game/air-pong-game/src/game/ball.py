class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 5  # Change in x (speed)
        self.dy = 5  # Change in y (speed)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        self.dy = -self.dy

    def reset_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_radius(self):
        return self.radius

    def check_collision(self, paddle):
        # Simple collision detection
        if (self.x + self.radius > paddle.x and
            self.x - self.radius < paddle.x + paddle.width and
            self.y + self.radius > paddle.y and
            self.y - self.radius < paddle.y + paddle.height):
            return True
        return False