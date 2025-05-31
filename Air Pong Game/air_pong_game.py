import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (144, 238, 144)  # Light green color for better eye comfort

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, img):
        cv2.circle(img, (int(self.x), int(self.y)), self.radius, self.color, -1)
        # Add a white border to make it more visible
        cv2.circle(img, (int(self.x), int(self.y)), self.radius, (255, 255, 255), 1)

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (147, 112, 219)  # Soft purple color for better eye comfort

    def draw(self, img):
        # Draw the main paddle
        cv2.rectangle(img, (int(self.x), int(self.y)), 
                     (int(self.x + self.width), int(self.y + self.height)), 
                     self.color, -1)
        # Add a white border to make it more visible
        cv2.rectangle(img, (int(self.x), int(self.y)), 
                     (int(self.x + self.width), int(self.y + self.height)), 
                     (255, 255, 255), 2)

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Air Pong Game")
        self.root.geometry("400x300")
        
        self.create_main_menu()
        
    def create_main_menu(self):
        # Main menu frame
        self.menu_frame = ttk.Frame(self.root, padding="20")
        self.menu_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(self.menu_frame, text="Air Pong Game", 
                              font=('Helvetica', 24, 'bold'))
        title_label.grid(row=0, column=0, pady=20)
        
        # Start button
        start_btn = ttk.Button(self.menu_frame, text="Start Game", 
                             command=self.start_game)
        start_btn.grid(row=1, column=0, pady=10)
        
        # Instructions button
        instructions_btn = ttk.Button(self.menu_frame, text="Instructions", 
                                    command=self.show_instructions)
        instructions_btn.grid(row=2, column=0, pady=10)
        
        # Quit button
        quit_btn = ttk.Button(self.menu_frame, text="Quit", 
                            command=self.root.quit)
        quit_btn.grid(row=3, column=0, pady=10)

    def show_instructions(self):
        messagebox.showinfo("Instructions",
            "1. Use your hand to control the paddle\n"
            "2. Move your index finger up and down\n"
            "3. Keep the ball in play\n"
            "4. Press 'Q' to quit the game"
        )

    def start_game(self):
        self.root.withdraw()  # Hide main menu
        game = Game()
        game.run()
        self.root.deiconify()  # Show main menu again when game ends

    def run(self):
        self.root.mainloop()

class Game:
    def __init__(self):
        self.detector = HandDetector()
        self.window_width = 1280
        self.window_height = 720
        self.paddle = Paddle(50, self.window_height//2 - 50, 20, 100)
        
        # Create three balls with different colors and starting positions
        self.balls = [
            Ball(self.window_width//2, self.window_height//2, 10, 7, 7),  # Original ball
            Ball(self.window_width//2, self.window_height//3, 10, -8, 6),  # Second ball
            Ball(self.window_width//2, 2*self.window_height//3, 10, 9, -7)  # Third ball
        ]
        # Set different colors for each ball
        self.balls[0].color = (144, 238, 144)  # Light green
        self.balls[1].color = (173, 216, 230)  # Light blue
        self.balls[2].color = (255, 218, 185)  # Peach
        
        self.score = 0
        self.game_over = False

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)
            img = cv2.resize(img, (self.window_width, self.window_height))
            img = self.detector.find_hands(img)
            lm_list = self.detector.find_position(img)

            if len(lm_list) > 0:
                self.paddle.y = lm_list[8][2] - self.paddle.height//2
                self.paddle.y = max(0, min(self.window_height - self.paddle.height, 
                                         self.paddle.y))

            if not self.game_over:
                self.update_game_state(img)
            self.draw_game(img)

            cv2.imshow('Air Pong', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def update_game_state(self, img):
        for ball in self.balls:
            ball.move()

            # Ball collision with walls
            if ball.y - ball.radius <= 0 or \
               ball.y + ball.radius >= self.window_height:
                ball.speed_y *= -1

            # Ball collision with paddle
            if (ball.x - ball.radius <= self.paddle.x + self.paddle.width and
                self.paddle.y <= ball.y <= self.paddle.y + self.paddle.height):
                ball.speed_x *= -1
                self.score += 1

            # Ball collision with right wall
            if ball.x + ball.radius >= self.window_width:
                ball.speed_x *= -1

            # Game over condition
            if ball.x - ball.radius <= 0:
                self.game_over = True

    def draw_game(self, img):
        self.paddle.draw(img)
        for ball in self.balls:
            ball.draw(img)
        
        # Display score in red color (BGR format)
        cv2.putText(img, f'Score: {self.score}', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if self.game_over:
            cv2.putText(img, 'Game Over!', 
                       (self.window_width//2 - 100, self.window_height//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

if __name__ == "__main__":
    game_gui = GameGUI()
    game_gui.run()