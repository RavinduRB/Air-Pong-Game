import unittest
from src.hand_tracking.hand_detector import HandDetector

class TestHandDetector(unittest.TestCase):

    def setUp(self):
        self.detector = HandDetector()

    def test_hand_detection(self):
        # Simulate an image input for hand detection
        image = ...  # Replace with actual image data
        hands = self.detector.detect_hands(image)
        self.assertIsNotNone(hands)
        self.assertGreater(len(hands), 0)

    def test_get_hand_positions(self):
        # Simulate an image input for getting hand positions
        image = ...  # Replace with actual image data
        hands = self.detector.detect_hands(image)
        positions = self.detector.get_hand_positions(hands)
        self.assertIsInstance(positions, list)
        self.assertGreater(len(positions), 0)

if __name__ == '__main__':
    unittest.main()