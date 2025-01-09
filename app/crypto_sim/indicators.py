import random
from typing import Dict, Tuple

class TechnicalIndicators:
    @staticmethod
    def generate_indicators(volume: float, market_data: Dict[str, float]) -> Dict[str, float]:
        """Generate simulated technical indicators based on market context.

        Args:
            volume (float): Current trading volume
            market_data (dict): Dictionary containing market context like price changes and volumes

        Returns:
            dict: Dictionary containing simulated technical indicators including:
                - RSI (Relative Strength Index)
                - MACD (Moving Average Convergence Divergence)
                - OBV (On Balance Volume)
                - Funding rate
                - CVD (Cumulative Volume Delta)
                - OI (Open Interest)
        """
        price_momentum: float = max(min(market_data['price_change_24h'] / 100, 1), -1)  # Limit to ±100%
        vol_ratio: float = max(min(volume / max(market_data['volume'] / 24, 1), 10), 0.1)  # Limit ratio between 0.1x and 10x
        
        return {
            'rsi': max(min(50 + price_momentum * 200 + random.uniform(-10, 10), 95), 5),
            'macd': max(min(price_momentum * 100 + random.uniform(-20, 20), 100), -100),
            'obv': max(volume * (1 + price_momentum) * random.uniform(0.8, 1.2), 1),  # Ensure minimum OBV of 1
            'funding': max(min(price_momentum * 0.1 + random.uniform(-0.05, 0.05), 0.2), -0.2),
            'cvd': max(min(volume * price_momentum * random.uniform(-0.3, 0.3), volume), -volume),
            'oi': max(volume * (1.5 + price_momentum) * random.uniform(0.4, 1.6), 1)  # Ensure minimum OI of 1
        }

    @staticmethod
    def generate_market_metrics(base_volatility: float, current_price: float, market_data: Dict[str, float]) -> Tuple[float, float]:
        """Generate simulated market movement metrics incorporating multiple timeframe cycles and influences."""
        # Multiple cycles to create more realistic movements
        long_cycle: float = random.uniform(-0.02, 0.02)    # 4-hour cycle
        medium_cycle: float = random.uniform(-0.015, 0.015)  # 1-hour cycle
        short_cycle: float = random.uniform(-0.01, 0.01)   # 15-minute cycle
        micro_cycle: float = random.uniform(-0.005, 0.005)  # 1-minute cycle
        
        # Trend based on recent price action
        trend: float = market_data['price_change_24h'] / 100 / 3600  # Distribute 24h change across hours
        
        # Support and resistance influences
        ath_influence: float = -0.001 * (market_data['ath'] - current_price) / market_data['ath']
        atl_influence: float = 0.001 * (current_price - market_data['atl']) / current_price
        
        # Combine all influences
        actual_volatility: float = base_volatility * (1 + abs(market_data['price_change_24h']) / 100)  # Normal volatility scaling
        price_change: float = (
            random.gauss(0, actual_volatility) +  # Random walk
            trend +  # Overall trend
            long_cycle + medium_cycle + short_cycle + micro_cycle +  # Market cycles
            ath_influence + atl_influence  # Support/resistance
        )
        
        # Volume tends to increase with volatility
        volume_multiplier: float = 1 + abs(price_change) * 2
        base_volume_change: float = random.gauss(0, 0.02)  # Base volume change
        volume_change: float = base_volume_change * volume_multiplier
        
        return price_change, volume_change
