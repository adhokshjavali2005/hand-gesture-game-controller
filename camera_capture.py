"""
camera_capture.py

Handles real-time webcam capture and frame management.
Provides continuous frame stream from the laptop camera.
"""

import cv2
import threading
from collections import deque
from typing import Tuple, Optional


class CameraCapture:
    """
    Manages webcam capture and frame buffering for real-time processing.
    Uses threading to ensure smooth frame capture without blocking.
    """

    def __init__(self, camera_id: int = 0, buffer_size: int = 2):
        """
        Initialize camera capture.

        Args:
            camera_id: Index of the camera device (default: 0 for built-in webcam)
            buffer_size: Number of frames to buffer (smaller = less latency)
        """
        self.camera_id = camera_id
        self.buffer_size = buffer_size
        self.cap = None
        self.frame_buffer = deque(maxlen=buffer_size)
        self.is_running = False
        self.capture_thread = None
        self.frame_width = 0
        self.frame_height = 0
        self.fps = 0

    def start(self) -> bool:
        """
        Start the camera and begin capturing frames.

        Returns:
            True if camera started successfully, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)

            if not self.cap.isOpened():
                print(f"Error: Cannot open camera with ID {self.camera_id}")
                return False

            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer for low latency
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            # Get actual frame dimensions
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()

            print(f"Camera started: {self.frame_width}x{self.frame_height} @ {self.fps} FPS")
            return True

        except Exception as e:
            print(f"Error starting camera: {e}")
            return False

    def _capture_loop(self):
        """
        Internal loop that continuously captures frames from the camera.
        Runs in a separate thread to prevent blocking.
        """
        while self.is_running:
            ret, frame = self.cap.read()

            if ret:
                # Flip frame horizontally for selfie-view (more natural for hand tracking)
                frame = cv2.flip(frame, 1)
                self.frame_buffer.append(frame)
            else:
                print("Error: Failed to capture frame")
                break

    def get_frame(self) -> Optional[Tuple[bool, any]]:
        """
        Get the most recent frame from the buffer.

        Returns:
            Tuple of (success: bool, frame: numpy array) or (False, None) if no frame available
        """
        if len(self.frame_buffer) > 0:
            return True, self.frame_buffer[-1]
        return False, None

    def stop(self):
        """Stop camera capture and clean up resources."""
        self.is_running = False

        if self.capture_thread:
            self.capture_thread.join(timeout=2)

        if self.cap:
            self.cap.release()

        print("Camera stopped")

    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions of captured frames.

        Returns:
            Tuple of (width, height)
        """
        return self.frame_width, self.frame_height
