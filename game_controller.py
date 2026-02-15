"""
game_controller.py

Sends keyboard input to control Hill Climb Racing game.
Handles press/release logic with smooth transitions to avoid flickering.
Uses pyautogui for better browser game compatibility.
"""

import pyautogui
import time
from typing import Tuple
from enum import Enum

# Disable pyautogui fail-safe (moving mouse to corner won't stop it)
pyautogui.FAILSAFE = False
# Reduce pause between actions for faster response
pyautogui.PAUSE = 0


class GameAction(Enum):
    """Enum for game actions."""
    ACCELERATE = "accelerate"
    BRAKE = "brake"
    IDLE = "idle"


class GameController:
    """
    Controls game input by simulating keyboard presses.
    Prevents key flickering through debouncing and state management.
    """

    def __init__(self, min_action_duration: float = 0.05):
        """
        Initialize game controller.

        Args:
            min_action_duration: Minimum time (seconds) to hold a key press (prevents flickering)
        """
        self.min_action_duration = min_action_duration

        # Key assignments (pyautogui uses string names)
        self.accelerate_key = 'right'  # Right Arrow for acceleration
        self.brake_key = 'left'  # Left Arrow for braking

        # State tracking
        self.current_action = GameAction.IDLE
        self.last_action_time = 0
        self.pressed_keys = set()

        print("Game controller initialized (using pyautogui for browser compatibility)")

    def send_action(self, gesture: str, is_confident: bool) -> GameAction:
        """
        Convert gesture to game action and send keyboard input.

        Args:
            gesture: 'open' (accelerate), 'closed' (brake), or 'uncertain'
            is_confident: Whether gesture confidence meets threshold

        Returns:
            The action performed (GameAction enum)
        """
        # Determine action from gesture
        if not is_confident or gesture == 'uncertain':
            desired_action = GameAction.IDLE
        elif gesture == 'open':
            desired_action = GameAction.ACCELERATE
        elif gesture == 'closed':
            desired_action = GameAction.BRAKE
        else:
            desired_action = GameAction.IDLE

        # Check if we should update the action based on minimum duration
        current_time = time.time()
        time_since_last_action = current_time - self.last_action_time

        if time_since_last_action >= self.min_action_duration:
            # Release previous action if different
            if self.current_action != desired_action:
                self._release_all_keys()
                self.current_action = desired_action

                # Press new action key
                if desired_action == GameAction.ACCELERATE:
                    self._press_key(self.accelerate_key)
                elif desired_action == GameAction.BRAKE:
                    self._press_key(self.brake_key)

                self.last_action_time = current_time

        return desired_action

    def _press_key(self, key):
        """
        Press and hold a key using pyautogui.

        Args:
            key: The key name to press (e.g., 'right', 'left')
        """
        try:
            pyautogui.keyDown(key)
            self.pressed_keys.add(key)
        except Exception as e:
            print(f"Error pressing key: {e}")

    def _release_key(self, key):
        """
        Release a pressed key.

        Args:
            key: The key name to release
        """
        try:
            pyautogui.keyUp(key)
            self.pressed_keys.discard(key)
        except Exception as e:
            print(f"Error releasing key: {e}")

    def _release_all_keys(self):
        """Release all currently pressed keys."""
        for key in list(self.pressed_keys):
            self._release_key(key)
        # Also explicitly release arrow keys to be safe
        try:
            pyautogui.keyUp('right')
            pyautogui.keyUp('left')
        except:
            pass

    def stop(self):
        """
        Stop all key presses and clean up.
        Call this when exiting the application.
        """
        self._release_all_keys()
        self.current_action = GameAction.IDLE
        print("Game controller stopped")

    def get_current_action(self) -> str:
        """
        Get the current action being performed.

        Returns:
            String representation of current action
        """
        return self.current_action.value

    def quick_press(self, key, duration: float = 0.1):
        """
        Quickly press and release a key (for future features).

        Args:
            key: The key name to press
            duration: How long to hold the key (seconds)
        """
        self._press_key(key)
        time.sleep(duration)
        self._release_key(key)
