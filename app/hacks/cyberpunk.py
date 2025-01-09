import random
import time
from colorama import Fore, Style
from dataclasses import dataclass
from . import BaseVisualConfig, BaseHackSimulator

@dataclass
class CyberpunkConfig(BaseVisualConfig):
    """Configuration class for cyberpunk-themed visual effects.
    
    Attributes:
        matrix_chars (str): String containing Japanese characters used in the matrix rain effect
    """
    matrix_chars: str = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"

class CyberpunkHack(BaseHackSimulator):
    """Simulates a cyberpunk-themed hacking sequence with matrix rain effects."""

    def get_config(self) -> CyberpunkConfig:
        """Returns the configuration for the cyberpunk visual effects.
        
        Returns:
            CyberpunkConfig: Configuration object with cyberpunk-specific settings
        """
        return CyberpunkConfig()

    def get_init_messages(self) -> list[str]:
        """Returns initialization messages displayed during startup.
        
        Returns:
            list[str]: List of cyberpunk-themed initialization messages
        """
        return [
            "INITIALIZING QUANTUM PROCESSORS",
            "ESTABLISHING SECURE CONNECTION",
            "LOADING NEURAL BYPASS MODULES", 
            "CALIBRATING ENCRYPTION MATRICES"
        ]

    def get_hack_messages(self) -> list[str]:
        """Returns messages displayed during the hacking sequence.
        
        Returns:
            list[str]: List of cyberpunk-themed hacking progress messages
        """
        return [
            "BYPASSING QUANTUM FIREWALL ENCRYPTION...",
            "INJECTING POLYMORPHIC PAYLOAD...",
            "DECRYPTING NEURAL DATABASE NODES...",
            "ACCESSING MAINFRAME CORE SYSTEMS...",
            "EXTRACTING ENCRYPTED DATA STREAMS...",
            "ROUTING THROUGH DARK WEB PROXIES...",
            "COMPILING ADVANCED AI ALGORITHMS...",
            "DEPLOYING STEALTH PROTOCOLS...",
            "BREACHING SECURITY LAYER ALPHA...",
            "INTERCEPTING NETWORK PACKETS..."
        ]

    def print_banner(self) -> None:
        """Prints the cyberpunk-themed banner with dramatic effect."""
        banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║          QUANTUM CYBERSECURITY MATRIX v4.0.1             ║
    ║     [ TOP SECRET ] - CLASSIFIED NEURAL INFILTRATION      ║
    ╚══════════════════════════════════════════════════════════╝
    """
        self.visual.dramatic_print(banner, Fore.GREEN, 0.001)

    def generate_matrix_line(self) -> str:
        """Generates a single line of matrix rain effect with random colored characters.
        
        Returns:
            str: A string of Japanese characters with color formatting
        """
        line = ''.join(random.choice(self.config.matrix_chars) for _ in range(self.config.line_length))
        colored_line = ''
        for char in line:
            if random.random() < self.config.bright_char_chance:  # chance for bright characters
                colored_line += Style.BRIGHT + Fore.WHITE + char
            else:
                colored_line += Style.NORMAL + Fore.GREEN + char
        return colored_line + Style.RESET_ALL

    def run_matrix_effect(self) -> None:
        """Runs the continuous matrix rain effect with intermittent hack messages."""
        while True:
            # Matrix rain effect
            for _ in range(random.randint(1, 5)):
                print(self.generate_matrix_line())
                time.sleep(random.uniform(*self.config.matrix_delay_range))
            
            msg = random.choice(self.hack_messages)
            print(Fore.CYAN + Style.BRIGHT + f"\r[*] {msg}", end="")
            time.sleep(0.7)

if __name__ == "__main__":
    hack = CyberpunkHack()
    hack.run() 