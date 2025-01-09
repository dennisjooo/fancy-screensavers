import math
import sys
import time
import random
from colorama import Fore, Style
from typing import Dict

from ...utils.base_simulator import BaseSimulator
from ...utils.formatting import format_time, format_number, print_header
from .config import LLMConfig
from .metrics import generate_training_metrics, generate_system_metrics

class LLMSimulator(BaseSimulator):
    """Simulates training of a large language model with realistic metrics and visualizations.
    
    This simulator provides a realistic training experience for large language models,
    including metrics tracking, system monitoring, error handling and training insights.
    """

    def __init__(self, config: LLMConfig):
        """Initialize the LLM simulator.
        
        Args:
            config (LLMConfig): Configuration object containing training parameters.
        """
        super().__init__()
        self.config = config
        self.tokens_per_step = config.batch_size * config.num_gpus * config.seq_length
        self.total_steps = int(config.total_tokens / self.tokens_per_step)
        self.steps_per_epoch = self.total_steps // config.max_epochs
        self.checkpoint_freq = 100
        
        self.error_templates = [
            (Fore.RED, "ERROR", [
                "CUDA out of memory. Attempting gradient checkpointing...",
                "Detected NaN loss. Skipping bad gradient update...",
                "GPU thermal throttling detected. Reducing compute...",
                "NCCL connection timeout. Retrying communication...",
                "Memory fragmentation detected. Attempting defrag...",
                "Critical memory leak detected. Initiating emergency cleanup...",
                "Tensor core utilization suboptimal. Recompiling kernels..."
            ], (3, 8)),
            (Fore.YELLOW, "WARN", [
                "Network throughput degraded. Reducing batch size...",
                "Communication overhead high. Adjusting all-reduce...",
                "Memory pressure detected. Increasing gradient accumulation...",
                "Node synchronization latency high. Adjusting timeout...",
                "Load imbalance detected. Rebalancing shards..."
            ], (2, 5)),
            (Fore.BLUE, "INFO", [
                "Auto-scaling group activated. Provisioning backup nodes...",
                "Dynamic voltage scaling engaged. Optimizing power/performance...",
                "Tensor parallelism reconfigured. Optimizing for locality...",
                "Pipeline schedule rebalanced. Adjusting micro-batches..."
            ], (1, 3))
        ]
    
    def generate_metrics(self, progress: float) -> Dict[str, float]:
        """Generate training metrics based on current progress."""
        return generate_training_metrics(progress)
    
    def generate_system_metrics(self) -> Dict[str, float]:
        """Generate system performance metrics."""
        return generate_system_metrics()
    
    def print_training_summary(self, epoch: int, step: int, tokens_seen: int, train_loss: float):
        """Print a summary of the training run.
        
        Args:
            epoch (int): Current training epoch
            step (int): Current step within epoch
            tokens_seen (int): Number of tokens processed in current epoch
            train_loss (float): Current training loss value
        """
        total_time = time.time() - self.start_time
        tokens_processed = tokens_seen + (epoch * self.steps_per_epoch * self.tokens_per_step)
        print(Fore.RED + Style.BRIGHT + "\n\n[!] Training interrupted" + Style.RESET_ALL)
        print(Fore.YELLOW + f"""
Training Summary:
{'='*50}
- Total runtime: {format_time(total_time)}
- Tokens processed: {format_number(tokens_processed)} ({(tokens_processed/self.config.total_tokens*100):.1f}% of target)
- Final loss: {train_loss:.4f} (Best: {self.best_metric:.4f})
- Average throughput: {format_number(tokens_processed/total_time)} tokens/second
- Checkpoints saved: {(epoch * self.steps_per_epoch + step) // self.checkpoint_freq}
- Model size: {format_number(self.config.num_params * 2)}B parameters
- Node stability: {random.randint(94, 99)}%
- Peak memory utilization: {random.uniform(90, 98):.1f}%
- Average GPU utilization: {random.uniform(92, 98):.1f}%
- Total power consumed: {random.uniform(250, 350):.1f} kWh
- Network data transferred: {format_number(random.uniform(1e15, 2e15))}B
        """ + Style.RESET_ALL)
    
    def run(self):
        """Run the LLM training simulation.
        
        This method executes the main training loop, displaying progress, metrics,
        system stats and training insights. The simulation can be interrupted with Ctrl+C.
        """
        config_items = {
            "Parameters": f"{format_number(self.config.num_params)} ({self.config.num_params:.2e})",
            "Context Length": self.config.seq_length,
            "Training Tokens": format_number(self.config.total_tokens),
            "Hardware": f"{self.config.num_gpus} A100 80GB GPUs ({self.config.num_nodes} nodes)",
            "Precision": f"{self.config.precision} with ZeRO-3",
            "Global Batch Size": self.config.batch_size * self.config.num_gpus,
            "Learning Rate": self.config.learning_rate,
            "Architecture": "Decoder-only Transformer",
            "Position Embedding": "Rotary",
            "Activation": "SwiGLU"
        }
        print_header(self.config.model_name, config_items)
        
        init_steps = [
            "Setting up DeepSpeed ZeRO-3 configuration",
            "Initializing model shards across nodes",
            "Compiling CUDA kernels for flash attention",
            "Loading tokenizer and vocabulary",
            "Preparing training dataset shards",
            "Optimizing memory access patterns",
            "Setting up gradient checkpointing",
            "Initializing optimizer states",
            "Configuring distributed data loaders",
            "Verifying node connectivity"
        ]
        self.initialize_environment(init_steps)
        self.start_time = time.time()
        
        try:
            for epoch in range(self.config.max_epochs):
                tokens_seen = 0
                
                for step in range(self.steps_per_epoch):
                    if random.random() < 0.08:
                        issue, delay = self.simulate_issue(self.error_templates)
                        print("\n" + issue)
                        time.sleep(delay * 2)
                    
                    tokens_seen += self.tokens_per_step
                    total_tokens_seen = tokens_seen + (epoch * self.steps_per_epoch * self.tokens_per_step)
                    metrics = self.generate_metrics(epoch + step/self.steps_per_epoch)
                    self.best_metric = min(self.best_metric, metrics['train_loss'])
                    
                    elapsed = time.time() - self.start_time
                    tokens_per_sec = total_tokens_seen / elapsed
                    eta = (self.config.total_tokens - total_tokens_seen) / tokens_per_sec
                    
                    status = f"""{Fore.CYAN}Step [{step:5d}/{self.steps_per_epoch}] | Loss: {metrics['train_loss']:.4f} | Tokens: {format_number(total_tokens_seen)} | {format_number(tokens_per_sec)}/sec | ETA: {format_time(eta)}{Style.RESET_ALL}"""
                    print(f"\r{status}", end="")
                    
                    if step % self.checkpoint_freq == 0 and step > 0:
                        print(f"\n{Fore.GREEN}[+] Saving checkpoint at step {step}...{Style.RESET_ALL}")
                        time.sleep(15)
                        print(f"{Fore.GREEN}[+] Checkpoint saved to: /checkpoints/atlas70b/epoch_{epoch}_step_{step}/{Style.RESET_ALL}")
                    
                    if step % 50 == 0:
                        system_metrics = self.generate_system_metrics()
                        formatters = {
                            'gpu_util': ("GPU Util    [{} {}] {:.1f}%", 100),
                            'gpu_temp': ("Temperature [{} {}] {:.1f}°C", 100),
                            'gpu_power': ("Power       [{} {}] {:.1f}W", 500),
                            'gpu_memory': ("Memory      [{} {}] {:.1f}GB/80GB", 80),
                            'network_bw': ("Network BW  [{} {}] {:.1f}GB/s", 25),
                            'nvlink_util': ("NVLink     [{} {}] {:.1f}%", 100),
                            'pcie_util': ("PCIe Util   [{} {}] {:.1f}%", 100),
                            'fan_speed': ("Fan Speed   [{} {}] {:.1f}%", 100)
                        }
                        metric_bars = self.format_metrics_bars(system_metrics, formatters)
                        
                        summary = f"""
{Fore.GREEN}{'='*100}
[Training Progress] {format_number(total_tokens_seen)}/{format_number(self.config.total_tokens)} tokens processed
{Fore.YELLOW}Training Metrics:
    Loss: {metrics['train_loss']:.4f} (Best: {self.best_metric:.4f})
    Perplexity: {metrics['perplexity']:.2f}
    Grad Norm: {random.uniform(0.1, 1.0):.3f}
    Tokens/Second: {format_number(tokens_per_sec)}
{Fore.CYAN}Validation Metrics:
    Loss: {metrics['val_loss']:.4f}
    Perplexity: {math.exp(metrics['val_loss']):.2f}
    Next Token Accuracy: {50 + random.uniform(0, 15):.2f}%
{Fore.MAGENTA}System State:
    {metric_bars['gpu_util']}
    {metric_bars['gpu_temp']}
    {metric_bars['gpu_power']}
    {metric_bars['gpu_memory']}
    {metric_bars['network_bw']}
    {metric_bars['nvlink_util']}
    {metric_bars['pcie_util']}
    {metric_bars['fan_speed']}
{Fore.BLUE}Training State:
    Learning Rate: {self.config.learning_rate * (0.95 ** (epoch + step/self.steps_per_epoch)):.2e}
    Active Nodes: {self.config.num_nodes - random.randint(0, 3)}/{self.config.num_nodes}
    Global Batch Utilization: {random.uniform(92, 99.5):.1f}%
    Grad Scaling: {2**random.randint(10,15)}
    Node Sync Rate: {random.uniform(95, 99.9):.1f}%{Style.RESET_ALL}"""
                        print(summary)
                        
                        insights = [
                            (f"{Fore.GREEN}[✓] Attention patterns stabilizing across nodes", 0.2),
                            (f"{Fore.GREEN}[✓] Token embeddings converging rapidly", 0.2),
                            (f"{Fore.YELLOW}[!] Gradient noise scale: {random.uniform(0.8, 1.2):.2f}", 0.3),
                            (f"{Fore.GREEN}[✓] Detected potential emergent abilities", 0.1),
                            (f"{Fore.BLUE}[i] Layer-wise gradients balanced", 0.2),
                            (f"{Fore.YELLOW}[!] Activation sparsity: {random.uniform(65, 75):.1f}%", 0.3)
                        ]
                        self.print_training_insights(insights)
                    
                    time.sleep(1.5)
        
        except KeyboardInterrupt:
            self.print_training_summary(epoch, step, tokens_seen, metrics['train_loss'])
            sys.exit(0) 