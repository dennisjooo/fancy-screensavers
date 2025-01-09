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
        price_momentum: float = market_data['price_change_24h'] / 100
        vol_ratio: float = volume / (market_data['volume'] / 24)
        
        return {
            'rsi': max(min(50 + price_momentum * 200 + random.uniform(-10, 10), 95), 5),
            'macd': price_momentum * 100 + random.uniform(-20, 20),
            'obv': volume * (1 + price_momentum) * random.uniform(0.8, 1.2),
            'funding': price_momentum * 0.1 + random.uniform(-0.05, 0.05),
            'cvd': volume * price_momentum * random.uniform(-0.3, 0.3),
            'oi': volume * (1.5 + price_momentum) * random.uniform(0.4, 1.6)
        }

    @staticmethod
    def generate_market_metrics(base_volatility: float, current_price: float, market_data: Dict[str, float]) -> Tuple[float, float]:
        """Generate simulated market movement metrics incorporating multiple timeframe cycles and influences.

        Args:
            base_volatility (float): Base volatility level for price movements
            current_price (float): Current market price
            market_data (dict): Dictionary containing market context like ATH, ATL and price changes

        Returns:
            tuple: Contains:
                - price_change (float): Calculated price change incorporating all influences
                - volume_change (float): Corresponding volume change based on volatility
        """
        # Multiple cycles to create more realistic movements
        long_cycle: float = random.uniform(-0.2, 0.2)  # 4-hour cycle
        medium_cycle: float = random.uniform(-0.15, 0.15)  # 1-hour cycle
        short_cycle: float = random.uniform(-0.1, 0.1)  # 15-minute cycle
        micro_cycle: float = random.uniform(-0.05, 0.05)  # 1-minute cycle
        
        # Trend based on recent price action
        trend: float = market_data['price_change_24h'] / 100 / 86400  # Distribute 24h change across seconds
        
        # Support and resistance influences
        ath_influence: float = -0.1 * (market_data['ath'] - current_price) / market_data['ath']
        atl_influence: float = 0.1 * (current_price - market_data['atl']) / current_price
        
        # Combine all influences
        actual_volatility: float = base_volatility * (1 + abs(market_data['price_change_24h']) / 100)
        price_change: float = (
            random.gauss(0, actual_volatility) +  # Random walk
            trend +  # Overall trend
            long_cycle + medium_cycle + short_cycle + micro_cycle +  # Market cycles
            ath_influence + atl_influence  # Support/resistance
        )
        
        # Volume tends to increase with volatility
        volume_multiplier: float = 1 + abs(price_change) * 5
        base_volume_change: float = random.gauss(0, 0.1)
        volume_change: float = base_volume_change * volume_multiplier
        
        return price_change, volume_change
