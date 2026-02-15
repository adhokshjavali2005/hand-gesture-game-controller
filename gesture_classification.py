"""
gesture_classification.py

Classifies hand gestures (open palm vs closed fist) based on landmarks.
Provides gesture confidence for smooth game control.
"""

import numpy as np
from typing import Tuple, Dict
import joblib
import os


class GestureClassifier:
    """
    Classifies hand gestures using hand metrics and ML model.
    Supports both rule-based and ML-based classification.
    """

    def __init__(self, use_ml_model: bool = False, model_path: str = None):
        """
        Initialize gesture classifier.

        Args:
            use_ml_model: If True, uses trained ML model; otherwise uses rule-based classification
            model_path: Path to trained model file (if use_ml_model is True)
        """
        self.use_ml_model = use_ml_model
        self.model = None
        self.model_scaler = None

        if use_ml_model and model_path and os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print(f"Loaded ML model from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}. Falling back to rule-based classification.")
                self.use_ml_model = False
        elif use_ml_model:
            print("ML model not found. Using rule-based classification.")
            self.use_ml_model = False

    def classify_gesture(self, hand_metrics: Dict) -> Tuple[str, float]:
        """
        Classify hand gesture as 'open' or 'closed'.

        Args:
            hand_metrics: Dictionary from HandDetector.get_hand_metrics()

        Returns:
            Tuple of (gesture: str, confidence: float)
                - gesture: 'open' for open palm, 'closed' for fist
                - confidence: Confidence score 0-1
        """
        if self.use_ml_model and self.model:
            return self._classify_with_model(hand_metrics)
        else:
            return self._classify_with_rules(hand_metrics)

    def _classify_with_rules(self, hand_metrics: Dict) -> Tuple[str, float]:
        """
        Rule-based gesture classification using hand metrics.

        Rules:
        - Open palm: Most fingers extended (3+ fingers up)
        - Closed fist: Most fingers curled (0-2 fingers up)
        """
        # Use finger extension states for more accurate detection
        extended_count = hand_metrics.get('extended_count', 0)
        fingers_extended = hand_metrics.get('fingers_extended', [])
        
        # Count extended fingers (excluding thumb for more reliable detection)
        # Index=1, Middle=2, Ring=3, Pinky=4 in fingers_extended list
        non_thumb_extended = sum(fingers_extended[1:]) if len(fingers_extended) > 1 else 0
        
        # Open palm: 3 or more non-thumb fingers extended
        # Closed fist: 1 or fewer non-thumb fingers extended
        if non_thumb_extended >= 3:
            # Open palm detected
            confidence = min(1.0, 0.5 + (non_thumb_extended / 8.0))
            return 'open', confidence
        elif non_thumb_extended <= 1:
            # Closed fist detected
            confidence = min(1.0, 0.6 + ((4 - non_thumb_extended) / 10.0))
            return 'closed', confidence
        else:
            # Ambiguous - 2 fingers extended
            # Fall back to distance-based check
            finger_distances = hand_metrics['finger_distances']
            hand_height = hand_metrics['hand_height']
            avg_distance = np.mean(finger_distances)
            threshold = 0.35 * hand_height
            
            if avg_distance > threshold:
                return 'open', 0.5
            else:
                return 'closed', 0.5

    def _classify_with_model(self, hand_metrics: Dict) -> Tuple[str, float]:
        """
        ML-based gesture classification using trained model.
        """
        # Extract features from hand metrics
        features = self._extract_features(hand_metrics)

        # Scale features if scaler is available
        if self.model_scaler:
            features = self.model_scaler.transform([features])
        else:
            features = np.array([features])

        # Get prediction and probability
        try:
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]

            # Get confidence (max probability)
            confidence = np.max(probabilities)

            gesture = 'open' if prediction == 1 else 'closed'
            return gesture, confidence
        except Exception as e:
            print(f"Error in model prediction: {e}")
            return self._classify_with_rules(hand_metrics)

    def _extract_features(self, hand_metrics: Dict) -> np.ndarray:
        """
        Extract features from hand metrics for ML model.

        Features:
        - Average finger distance
        - Finger distance variance
        - Hand aspect ratio
        - Individual finger distances
        """
        finger_distances = np.array(hand_metrics['finger_distances'])
        hand_height = hand_metrics['hand_height']
        hand_width = hand_metrics['hand_width']

        # Calculate features
        avg_distance = np.mean(finger_distances)
        distance_variance = np.var(finger_distances)
        aspect_ratio = hand_width / (hand_height + 1e-6)

        # Normalize by hand height
        normalized_distances = finger_distances / (hand_height + 1e-6)

        # Combine all features
        features = np.concatenate([
            [avg_distance / hand_height],
            [distance_variance / (hand_height ** 2)],
            [aspect_ratio],
            normalized_distances
        ])

        return features

    def smooth_gesture(self, gesture: str, confidence: float, confidence_threshold: float = 0.6) -> Tuple[str, bool]:
        """
        Apply confidence threshold to smooth gesture detection and prevent flickering.

        Args:
            gesture: Detected gesture ('open' or 'closed')
            confidence: Confidence score (0-1)
            confidence_threshold: Minimum confidence to register gesture

        Returns:
            Tuple of (gesture: str, is_confident: bool)
                - gesture: 'open', 'closed', or 'uncertain'
                - is_confident: True if confidence > threshold
        """
        if confidence < confidence_threshold:
            return 'uncertain', False

        return gesture, True

    def extract_vertical_position(self, hand_metrics: Dict) -> float:
        """
        Extract vertical position of hand (for potential future use).

        Args:
            hand_metrics: Dictionary from HandDetector.get_hand_metrics()

        Returns:
            Normalized vertical position (0.0 = top, 1.0 = bottom)
        """
        bbox = hand_metrics['bounding_box']
        # Assuming frame height is typically around 480
        # This should be normalized properly with actual frame height
        y_center = bbox[1] + (bbox[3] / 2)
        normalized_y = y_center / 480.0  # Placeholder - should use actual frame height
        return normalized_y

    def train_model(self, X_train: np.ndarray, y_train: np.ndarray, model_path: str):
        """
        Train a simple classifier on collected gesture data.

        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (0 = closed, 1 = open)
            model_path: Path to save the trained model
        """
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        # Create and train model
        self.model_scaler = StandardScaler()
        X_scaled = self.model_scaler.fit_transform(X_train)

        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_scaled, y_train)

        # Save model
        joblib.dump(self.model, model_path)
        joblib.dump(self.model_scaler, model_path.replace('.pkl', '_scaler.pkl'))

        print(f"Model trained and saved to {model_path}")
