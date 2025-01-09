from dataclasses import dataclass

@dataclass
class SegmentationConfig:
    """Configuration class for semantic segmentation model training simulation.
    
    Attributes:
        model_name (str): Name of the segmentation model. Defaults to "DeepSeg-L".
        architecture (str): Model architecture type. Defaults to "UNet++".
        backbone (str): Backbone network architecture. Defaults to "EfficientNetV2-L".
        max_epochs (int): Maximum number of training epochs. Defaults to 100.
        batch_size (int): Training batch size. Defaults to 16.
        image_size (int): Input image resolution. Defaults to 768.
        learning_rate (float): Initial learning rate. Defaults to 1e-4.
        num_classes (int): Number of segmentation classes. Defaults to 20.
        dataset_size (int): Total number of training images. Defaults to 50000.
        precision (str): Training precision mode. Defaults to "mixed_float16".
    """
    model_name: str = "DeepSeg-L"
    architecture: str = "UNet++"
    backbone: str = "EfficientNetV2-L"
    max_epochs: int = 100
    batch_size: int = 16
    image_size: int = 768
    learning_rate: float = 1e-4
    num_classes: int = 20
    dataset_size: int = 50000
    precision: str = "mixed_float16" 