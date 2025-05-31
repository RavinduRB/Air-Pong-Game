class HandDetector:
    def __init__(self, static_image_mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        import mediapipe as mp
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,
                                         max_num_hands=max_hands,
                                         min_detection_confidence=min_detection_confidence,
                                         min_tracking_confidence=min_tracking_confidence)

    def find_hands(self, image):
        import cv2
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        return results

    def get_hand_positions(self, results):
        if results.multi_hand_landmarks:
            hand_positions = []
            for hand_landmarks in results.multi_hand_landmarks:
                hand_positions.append([(lm.x, lm.y) for lm in hand_landmarks.landmark])
            return hand_positions
        return None

    def release(self):
        self.hands.close()