import sys
import time
from colorama import Fore, Style, init
from dataclasses import dataclass
from typing import List

# Initialize colorama for Windows compatibility
init()

@dataclass
class BaseVisualConfig:
    """Configuration class for visual effects in hack simulations.

    Attributes:
        progress_bar_width (int): Width of the progress bar in characters. Defaults to 40.
        default_text_delay (float): Default delay between characters when printing text. Defaults to 0.03.
        matrix_delay_range (tuple): Range of delays (min, max) for matrix effect. Defaults to (0.01, 0.4).
        line_length (int): Maximum length of text lines. Defaults to 70.
        bright_char_chance (float): Probability of a character being bright in matrix effect. Defaults to 0.1.
    """
    progress_bar_width: int = 40
    default_text_delay: float = 0.03
    matrix_delay_range: tuple = (0.01, 0.4)
    line_length: int = 70
    bright_char_chance: float = 0.1

class BaseVisualEffects:
    """Base class providing visual effects for hack simulations."""

    @staticmethod
    def progress_bar(progress: float, width: int = 40) -> str:
        """Generate a text-based progress bar.

        Args:
            progress (float): Progress value between 0 and 1.
            width (int, optional): Width of the progress bar. Defaults to 40.

        Returns:
            str: Progress bar string with percentage.
        """
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f'[{bar}] {int(progress * 100)}%'

    @staticmethod
    def dramatic_print(text: str, color: str = Fore.GREEN, delay: float = 0.03) -> None:
        """Print text dramatically with color and delay between characters.

        Args:
            text (str): Text to print.
            color (str, optional): Color to use. Defaults to Fore.GREEN.
            delay (float, optional): Delay between characters in seconds. Defaults to 0.03.
        """
        for char in text:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)

class BaseHackSimulator:
    """Base class for hack simulation implementations."""

    def __init__(self):
        """Initialize the hack simulator with configuration and visual effects."""
        self.config = self.get_config()
        self.visual = self.get_visual_effects()
        self.init_messages = self.get_init_messages()
        self.hack_messages = self.get_hack_messages()

    def get_config(self) -> BaseVisualConfig:
        """Get the visual configuration.

        Returns:
            BaseVisualConfig: Default visual configuration.
        """
        return BaseVisualConfig()

    def get_visual_effects(self) -> BaseVisualEffects:
        """Get the visual effects handler.

        Returns:
            BaseVisualEffects: Visual effects implementation.
        """
        return BaseVisualEffects()

    def get_init_messages(self) -> List[str]:
        """Get initialization messages.

        Returns:
            List[str]: List of initialization messages.
        """
        return []

    def get_hack_messages(self) -> List[str]:
        """Get hack sequence messages.

        Returns:
            List[str]: List of hack sequence messages.
        """
        return []

    def print_banner(self) -> None:
        """Print the hack simulator banner."""
        pass

    def run_initialization(self) -> None:
        """Run the initialization sequence with progress bars."""
        for msg in self.init_messages:
            print(Fore.YELLOW + f"\r[*] {msg}", end="")
            for i in range(101):
                print(f"\r[*] {msg}: {self.visual.progress_bar(i/100)}", end="")
                time.sleep(0.01)
            print()
        
        print(Fore.GREEN + "\n[+] SYSTEM INITIALIZED - COMMENCING SEQUENCE\n" + Style.RESET_ALL)
        time.sleep(1)

    def generate_matrix_line(self) -> str:
        """Generate a line for matrix rain effect.

        Returns:
            str: Generated matrix line.
        """
        return ""

    def run_matrix_effect(self) -> None:
        """Run the matrix rain effect animation."""
        pass

    def handle_interrupt(self) -> None:
        """Handle keyboard interrupt by displaying termination message and exiting."""
        print(Fore.RED + Style.BRIGHT + "\n\n[!] EMERGENCY PROTOCOL ACTIVATED - SYSTEM TERMINATED" + Style.RESET_ALL)
        self.visual.dramatic_print("* * * CONNECTION TERMINATED * * *", Fore.RED, 0.05)
        sys.exit(0)

    def run(self) -> None:
        """Run the complete hack simulation sequence."""
        try:
            self.print_banner()
            self.run_initialization()
            self.run_matrix_effect()
        except KeyboardInterrupt:
            self.handle_interrupt() 
            
from .cyberpunk import CyberpunkHack
from .pentest import PentestHack

def cyber_hack():
    """Run the cyberpunk-themed hack simulation."""
    CyberpunkHack().run()

def pentest_hack():
    """Run the penetration testing hack simulation."""
    PentestHack().run()
    
__all__ = ['cyber_hack', 'pentest_hack']