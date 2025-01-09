import time
from colorama import Fore, Style

def progress_bar(progress, width=40):
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}] {int(progress * 100)}%'

def format_number(num):
    if num >= 1e12:
        return f"{num/1e12:.2f}T"
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    if num >= 1e6:
        return f"{num/1e6:.2f}M"
    return f"{num:.2f}K"

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def print_header(title, config_items):
    header = f"""
    ╔════════════════════════════════════════════════════════════════╗
    ║                {title} Training Pipeline              
    ║     [Model Configuration]"""
    
    for key, value in config_items.items():
        header += f"\n    ║     - {key}: {value}"
    
    header += "\n    ╚════════════════════════════════════════════════════════════════╝\n"
    
    print(Fore.GREEN + Style.BRIGHT + header + Style.RESET_ALL) 