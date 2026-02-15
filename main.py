"""
main.py

Main orchestration script for hand gesture-controlled Hill Climb Racing.
Integrates all modules: camera capture, hand detection, gesture classification, and game control.

Usage:
    python main.py [--use-ml-model] [--model-path path/to/model.pkl]

Key bindings during execution:
    Q or ESC: Quit the application
    SPACE: Pause/resume gesture control
"""

import cv2
import argparse
import sys
from time import time

from camera_capture import CameraCapture
from hand_detection import HandDetector
from gesture_classification import GestureClassifier
from game_controller import GameController, GameAction


class HandGestureGameController:
    """
    Main coordinator for the hand gesture game controller system.
    Orchestrates all components and handles the main event loop.
    """

    def __init__(self, use_ml_model: bool = False, model_path: str = None, confidence_threshold: float = 0.6):
        """
        Initialize the gesture controller system.

        Args:
            use_ml_model: Whether to use ML model for gesture classification
            model_path: Path to ML model file
            confidence_threshold: Minimum confidence to register gesture
        """
        self.camera = CameraCapture(camera_id=0, buffer_size=2)
        self.hand_detector = HandDetector(max_num_hands=1, min_detection_confidence=0.5)
        self.gesture_classifier = GestureClassifier(use_ml_model=use_ml_model, model_path=model_path)
        self.game_controller = GameController(min_action_duration=0.05)

        self.confidence_threshold = confidence_threshold
        self.is_running = True
        self.is_paused = False

        # Statistics
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time()
        self.last_gesture = "uncertain"
        self.last_confidence = 0.0
        self.last_action = GameAction.IDLE

        print("Hand Gesture Game Controller initialized")
        print(f"Confidence threshold: {confidence_threshold}")
        print(f"ML Model: {'Enabled' if use_ml_model else 'Disabled (using rule-based)'}")

    def run(self):
        """Main execution loop for real-time gesture control."""
        if not self.camera.start():
            print("Failed to start camera. Exiting.")
            return

        print("\n" + "=" * 60)
        print("Hand Gesture Game Controller - STARTED")
        print("=" * 60)
        print("\nControls:")
        print("  - Open Palm → Accelerate (Right Arrow)")
        print("  - Closed Fist → Brake (Left Arrow)")
        print("  - SPACE: Pause/Resume")
        print("  - Q or ESC: Quit")
        print("\n" + "=" * 60 + "\n")

        while self.is_running:
            # Get frame from camera
            success, frame = self.camera.get_frame()

            if not success or frame is None:
                continue

            # Detect hands in frame
            hand_found, hand_data = self.hand_detector.detect_hands(frame)

            # Process detected hand
            if hand_found and not self.is_paused:
                # Extract metrics
                hand_metrics = self.hand_detector.get_hand_metrics(hand_data)

                # Classify gesture
                gesture, confidence = self.gesture_classifier.classify_gesture(hand_metrics)

                # Apply confidence threshold
                gesture, is_confident = self.gesture_classifier.smooth_gesture(
                    gesture, confidence, self.confidence_threshold
                )

                # Send to game controller
                if is_confident:
                    self.last_action = self.game_controller.send_action(gesture, is_confident)
                    self.last_gesture = gesture
                    self.last_confidence = confidence
                else:
                    self.game_controller.send_action(gesture, is_confident)
                    self.last_gesture = "uncertain"

                # Draw hand landmarks on frame
                frame = self.hand_detector.draw_landmarks(frame, hand_data)

            else:
                # No hand or paused
                if self.is_paused:
                    self.game_controller.send_action('uncertain', False)

            # Update and display statistics
            self.frame_count += 1
            current_time = time()
            if current_time - self.last_fps_time >= 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_fps_time = current_time

            # Render UI on frame
            frame = self._render_ui(frame, hand_found)

            # Display frame
            cv2.imshow('Hand Gesture Game Controller', frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # Q or ESC
                self.is_running = False
            elif key == ord(' '):  # SPACE
                self.is_paused = not self.is_paused
                status = "PAUSED" if self.is_paused else "RUNNING"
                print(f"\n>>> Gesture control {status}")

        self._cleanup()

    def _render_ui(self, frame, hand_found: bool):
        """
        Render UI information on the frame.

        Args:
            frame: The video frame
            hand_found: Whether a hand was detected

        Returns:
            Frame with rendered UI
        """
        frame_height, frame_width = frame.shape[:2]

        # FPS counter (top-left)
        cv2.putText(frame, f"FPS: {self.fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Hand detection status (top-right)
        if hand_found:
            status_text = "Hand Detected"
            status_color = (0, 255, 0)
        else:
            status_text = "No Hand"
            status_color = (0, 0, 255)

        cv2.putText(frame, status_text, (frame_width - 250, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        # Gesture and confidence (bottom-left)
        gesture_text = f"Gesture: {self.last_gesture.upper()}"
        cv2.putText(frame, gesture_text, (10, frame_height - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        confidence_text = f"Confidence: {self.last_confidence:.2f}"
        cv2.putText(frame, confidence_text, (10, frame_height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Current action (bottom-right)
        action_text = f"Action: {self.last_action.value.upper()}"
        action_color = (0, 255, 0) if self.last_action != GameAction.IDLE else (128, 128, 128)
        cv2.putText(frame, action_text, (frame_width - 300, frame_height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, action_color, 2)

        # Pause status (center)
        if self.is_paused:
            cv2.putText(frame, "[PAUSED]", (frame_width // 2 - 80, frame_height // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        return frame

    def _cleanup(self):
        """Clean up resources and stop all processes."""
        print("\n>>> Shutting down...")
        self.camera.stop()
        self.game_controller.stop()
        cv2.destroyAllWindows()
        print(">>> Cleanup complete. Goodbye!")


def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Hand gesture-controlled Hill Climb Racing game using MediaPipe and OpenCV"
    )
    parser.add_argument(
        "--use-ml-model",
        action="store_true",
        help="Use trained ML model for gesture classification"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="models/gesture_model.pkl",
        help="Path to trained ML model file (default: models/gesture_model.pkl)"
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.6,
        help="Minimum confidence threshold for gesture detection (default: 0.6)"
    )

    args = parser.parse_args()

    try:
        # Create and run controller
        controller = HandGestureGameController(
            use_ml_model=args.use_ml_model,
            model_path=args.model_path,
            confidence_threshold=args.confidence_threshold
        )
        controller.run()

    except KeyboardInterrupt:
        print("\n\n>>> Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n>>> Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
