import math
import random
from typing import Dict

def generate_training_metrics(progress: float) -> Dict[str, float]:
    """Generate training metrics based on current progress.
    
    Args:
        progress (float): Training progress from 0 to 1.
        
    Returns:
        Dict[str, float]: Dictionary containing training metrics.
    """
    train_loss = 2.8 * math.exp(-progress * 1.2) + random.uniform(0.01, 0.03)
    val_loss = train_loss + random.uniform(0.02, 0.08)
    perplexity = math.exp(train_loss)
    return {
        'train_loss': train_loss,
        'val_loss': val_loss,
        'perplexity': perplexity
    }

def generate_system_metrics() -> Dict[str, float]:
    """Generate system performance metrics.
    
    Returns:
        Dict[str, float]: Dictionary containing system metrics.
    """
    return {
        'gpu_util': random.uniform(85, 99),
        'gpu_temp': random.uniform(65, 85),
        'gpu_power': random.uniform(275, 400),
        'gpu_memory': random.uniform(65, 78),
        'network_bw': random.uniform(20, 25),
        'nvlink_util': random.uniform(80, 95),
        'pcie_util': random.uniform(70, 90),
        'fan_speed': random.uniform(70, 100)
    } 