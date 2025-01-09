import sys
import time
import random
from colorama import Fore, Style
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

from .formatting import format_time, format_number, progress_bar

class BaseSimulator(ABC):
    def __init__(self):
        self.start_time = None
        self.best_metric = float('inf')
    
    def initialize_environment(self, init_steps: List[str]):
        print(Fore.YELLOW + "[*] Initializing training environment..." + Style.RESET_ALL)
        
        for step in init_steps:
            print(Fore.BLUE + f"\r[*] {step}", end="")
            for i in range(101):
                print(f"\r[*] {step}: {progress_bar(i/100)}", end="")
                time.sleep(0.05)
            print()
            if random.random() < 0.3:
                print(Fore.YELLOW + f"[WARN] Retrying {step.lower()} (Attempt {random.randint(1,3)}/3)" + Style.RESET_ALL)
                time.sleep(3)
        
        print(Fore.GREEN + "\n[+] Environment initialized - Beginning training\n" + Style.RESET_ALL)
        time.sleep(2)
    
    def simulate_issue(self, error_templates: List[Tuple]) -> Tuple[str, float]:
        color, level, messages, delay_range = random.choice(error_templates)
        message = random.choice(messages)
        
        timestamp = time.strftime("%H:%M:%S.%f")[:-4]
        perf_impact = f" [Performance impact: {random.randint(5,30)}%]" if random.random() < 0.3 else ""
        recovery_time = f" [ETA: {random.randint(10,300)}s]" if random.random() < 0.3 else ""
        
        formatted_message = f"{color}[{timestamp}] [{level}]: {message}{perf_impact}{recovery_time}"
        formatted_message += Style.RESET_ALL
        
        return (formatted_message, random.uniform(delay_range[0], delay_range[1]))
    
    def format_metrics_bars(self, metrics: Dict[str, float], formatters: Dict[str, Tuple[str, float]]) -> Dict[str, str]:
        return {
            key: formatter[0].format(
                progress_bar(metrics[key]/100 if key.endswith('util') else metrics[key]/formatter[1], 20),
                progress_bar(metrics[key]/100 if key.endswith('util') else metrics[key]/formatter[1], 20),
                metrics[key]
            )
            for key, formatter in formatters.items()
            if key in metrics
        }
    
    def print_training_insights(self, insights: List[Tuple[str, float]], max_insights: int = 2):
        selected_insights = []
        for insight, prob in insights:
            if random.random() < prob and len(selected_insights) < max_insights:
                selected_insights.append(insight)
        
        if selected_insights:
            print("\nTraining Insights:")
            for insight in selected_insights:
                print(f"  {insight}{Style.RESET_ALL}")
                time.sleep(0.5)
    
    @abstractmethod
    def generate_metrics(self, progress: float) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def generate_system_metrics(self) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def print_training_summary(self):
        pass
    
    @abstractmethod
    def run(self):
        pass 