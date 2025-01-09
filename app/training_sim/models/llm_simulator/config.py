from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration class for large language model training simulation.
    
    Attributes:
        model_name (str): Name of the language model. Defaults to "Atlas-70B".
        num_params (float): Number of model parameters. Defaults to 70B.
        max_epochs (int): Maximum number of training epochs. Defaults to 3.
        batch_size (int): Per-GPU batch size. Defaults to 2048.
        seq_length (int): Maximum sequence length. Defaults to 4096.
        learning_rate (float): Initial learning rate. Defaults to 1e-5.
        total_tokens (float): Total training tokens target. Defaults to 4.5T.
        num_gpus (int): Total number of GPUs. Defaults to 1024.
        num_nodes (int): Number of compute nodes. Defaults to 128.
        precision (str): Training precision mode. Defaults to "bfloat16".
    """
    model_name: str = "Atlas-70B"
    num_params: float = 70e9
    max_epochs: int = 3
    batch_size: int = 2048
    seq_length: int = 4096
    learning_rate: float = 1e-5
    total_tokens: float = 4.5e12  # 4.5 trillion tokens
    num_gpus: int = 1024
    num_nodes: int = 128  # 8 GPUs per node
    precision: str = "bfloat16" 