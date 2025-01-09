from .models.llm_simulator import LLMSimulator, LLMConfig
from .models.segmentation_simulator import SegmentationSimulator, SegmentationConfig

def llm_sim():
    config = LLMConfig()
    simulator = LLMSimulator(config)
    simulator.run()

def segment_sim():
    config = SegmentationConfig()
    simulator = SegmentationSimulator(config)
    simulator.run()