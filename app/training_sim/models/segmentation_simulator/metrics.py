import math
import random
from typing import Dict

def generate_training_metrics(progress: float) -> Dict[str, float]:
    """Generate training metrics based on current progress.
    
    Args:
        progress (float): Current training progress from 0 to 1.
        
    Returns:
        Dict[str, float]: Dictionary containing dice score, IoU score and pixel accuracy.
    """
    dice_score = 0.5 + 0.35 * (1 - math.exp(-2 * progress)) + random.uniform(0.01, 0.03)
    iou_score = dice_score / (2 - dice_score) + random.uniform(-0.02, 0.02)
    pixel_acc = 0.7 + 0.25 * (1 - math.exp(-2 * progress)) + random.uniform(0.01, 0.02)
    return {
        'dice_score': dice_score,
        'iou_score': iou_score,
        'pixel_acc': pixel_acc
    }

def generate_system_metrics() -> Dict[str, float]:
    """Generate system performance metrics.
    
    Returns:
        Dict[str, float]: Dictionary containing GPU and timing metrics.
    """
    return {
        'gpu_util': random.uniform(85, 99),
        'gpu_temp': random.uniform(65, 85),
        'gpu_power': random.uniform(200, 300),
        'gpu_memory': random.uniform(12, 15),
        'batch_time': random.uniform(0.8, 1.2),
        'data_load': random.uniform(0.1, 0.3),
        'aug_time': random.uniform(0.2, 0.4)
    } 