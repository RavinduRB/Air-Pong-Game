import cv2
from game.game import Game
from hand_tracking.hand_detector import HandDetector

def main():
    # Initialize the hand detector
    hand_detector = HandDetector()

    # Create a game instance
    game = Game(hand_detector)

    # Start the game loop
    while True:
        game.update()
        game.render()

        # Exit the game if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()