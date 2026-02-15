"""
hand_detection.py

Uses MediaPipe to detect hand landmarks in real-time.
Provides hand position, landmarks, and hand-specific features.
"""

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from typing import Tuple, Optional, List, Dict
import cv2
import urllib.request
import os


class HandDetector:
    """
    Detects hand landmarks using MediaPipe's hand tracking solution (Tasks API).
    Provides landmarks, hand position, and additional metrics.
    """

    MODEL_PATH = "hand_landmarker.task"
    MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

    def __init__(self, static_image_mode: bool = False, max_num_hands: int = 1, min_detection_confidence: float = 0.7):
        """
        Initialize hand detector with MediaPipe Tasks API.

        Args:
            static_image_mode: If False, uses video mode (default for real-time)
            max_num_hands: Maximum number of hands to detect (default: 1)
            min_detection_confidence: Minimum confidence for hand detection (0-1)
        """
        # Download model if not exists
        self._download_model()

        # Create hand landmarker options
        base_options = python.BaseOptions(model_asset_path=self.MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE if static_image_mode else vision.RunningMode.IMAGE,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        print("Hand detector initialized with MediaPipe Tasks API")

    def _download_model(self):
        """Download the hand landmarker model if not present."""
        if not os.path.exists(self.MODEL_PATH):
            print(f"Downloading hand landmarker model...")
            urllib.request.urlretrieve(self.MODEL_URL, self.MODEL_PATH)
            print(f"Model downloaded to {self.MODEL_PATH}")

    def detect_hands(self, frame: np.ndarray) -> Tuple[bool, Optional[Dict]]:
        """
        Detect hands in the given frame.

        Args:
            frame: Input frame from camera (numpy array, BGR format)

        Returns:
            Tuple of (hand_found: bool, hand_data: dict) where hand_data contains:
                - landmarks: List of 21 hand landmarks (x, y, z coordinates)
                - handedness: 'Left' or 'Right'
                - confidence: Detection confidence
                - bounding_box: Approximate (x, y, width, height) of hand
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect hands
        results = self.detector.detect(mp_image)

        if results.hand_landmarks and len(results.hand_landmarks) > 0:
            # Get the first hand detected
            landmarks_data = results.hand_landmarks[0]
            handedness_data = results.handedness[0][0] if results.handedness else None

            # Extract landmark coordinates
            landmark_list = []
            frame_height, frame_width, _ = frame.shape

            for landmark in landmarks_data:
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                z = landmark.z
                landmark_list.append((x, y, z))

            # Calculate bounding box
            x_coords = [lm[0] for lm in landmark_list]
            y_coords = [lm[1] for lm in landmark_list]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            bbox = (x_min, y_min, x_max - x_min, y_max - y_min)

            # Get handedness and confidence
            handedness = handedness_data.category_name if handedness_data else "Unknown"
            confidence = handedness_data.score if handedness_data else 0.5

            hand_data = {
                'landmarks': landmark_list,
                'handedness': handedness,
                'confidence': confidence,
                'bounding_box': bbox
            }

            return True, hand_data

        return False, None

    def draw_landmarks(self, frame: np.ndarray, hand_data: Dict) -> np.ndarray:
        """
        Draw hand landmarks on the frame for visualization.

        Args:
            frame: Input frame
            hand_data: Hand detection data from detect_hands()

        Returns:
            Frame with drawn landmarks
        """
        landmarks = hand_data['landmarks']

        # Draw circles for each landmark
        for i, (x, y, z) in enumerate(landmarks):
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Draw connections between landmarks (fingers)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky
        ]

        for start, end in connections:
            x1, y1, _ = landmarks[start]
            x2, y2, _ = landmarks[end]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return frame

    def get_hand_metrics(self, hand_data: Dict) -> Dict:
        """
        Extract useful metrics from hand landmarks.

        Args:
            hand_data: Hand detection data from detect_hands()

        Returns:
            Dictionary containing:
                - palm_center: (x, y) center of palm
                - finger_distances: List of distances between fingertips and palm
                - fingers_extended: List of booleans for each finger (True if extended)
                - extended_count: Number of fingers extended
                - hand_height: Height of hand bounding box
                - hand_width: Width of hand bounding box
        """
        landmarks = hand_data['landmarks']
        bbox = hand_data['bounding_box']

        # Palm center (approximately landmark 0 - wrist)
        palm_center = (landmarks[0][0], landmarks[0][1])

        # Fingertip indices: 4 (thumb), 8 (index), 12 (middle), 16 (ring), 20 (pinky)
        fingertips = [4, 8, 12, 16, 20]
        finger_distances = []

        for tip_idx in fingertips:
            tip_x, tip_y, _ = landmarks[tip_idx]
            palm_x, palm_y = palm_center
            distance = np.sqrt((tip_x - palm_x) ** 2 + (tip_y - palm_y) ** 2)
            finger_distances.append(distance)

        # Determine which fingers are extended
        # For each finger, compare TIP position to PIP (or IP for thumb)
        # In image coordinates, lower y = higher position
        fingers_extended = []
        
        # Thumb: Compare TIP (4) to IP (3) - use x-coordinate for thumb
        # For right hand: extended if tip_x > ip_x; for left: tip_x < ip_x
        # Use distance from wrist as simpler approach
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        # Thumb is extended if tip is far from MCP
        thumb_extended = np.sqrt((thumb_tip[0] - thumb_mcp[0])**2 + (thumb_tip[1] - thumb_mcp[1])**2) > \
                        np.sqrt((thumb_ip[0] - thumb_mcp[0])**2 + (thumb_ip[1] - thumb_mcp[1])**2) * 0.8
        fingers_extended.append(thumb_extended)
        
        # Index finger: TIP (8) vs PIP (6) - extended if tip_y < pip_y (higher up)
        index_extended = landmarks[8][1] < landmarks[6][1]
        fingers_extended.append(index_extended)
        
        # Middle finger: TIP (12) vs PIP (10)
        middle_extended = landmarks[12][1] < landmarks[10][1]
        fingers_extended.append(middle_extended)
        
        # Ring finger: TIP (16) vs PIP (14)
        ring_extended = landmarks[16][1] < landmarks[14][1]
        fingers_extended.append(ring_extended)
        
        # Pinky finger: TIP (20) vs PIP (18)
        pinky_extended = landmarks[20][1] < landmarks[18][1]
        fingers_extended.append(pinky_extended)
        
        extended_count = sum(fingers_extended)

        hand_height = bbox[3]
        hand_width = bbox[2]

        metrics = {
            'palm_center': palm_center,
            'finger_distances': finger_distances,
            'fingers_extended': fingers_extended,
            'extended_count': extended_count,
            'hand_height': hand_height,
            'hand_width': hand_width,
            'bounding_box': bbox,
            'landmarks': landmarks
        }

        return metrics
