import random
import time
from colorama import Fore, Style
from typing import List, Tuple, Dict, Any
from .display import DisplayUtils

class MarketEvents:
    """Class for generating and managing market events and signals."""

    def __init__(self):
        """Initialize MarketEvents with DisplayUtils instance."""
        self.display: DisplayUtils = DisplayUtils()

    def simulate_market_event(self, current_price: float, market_data: Dict[str, Any]) -> Tuple[str, float]:
        """Generate and format market events based on current market conditions.

        Args:
            current_price (float): Current market price
            market_data (dict): Dictionary containing market data like price, volume, ATH, ATL etc.

        Returns:
            tuple: Formatted event message string and delay time (float)
        """
        # Use market context to determine event probabilities
        if market_data['price'] > market_data['ath'] * 0.95:
            event_weights: List[float] = [0.5, 0.3, 0.2]  # Higher chance of bearish events
        elif market_data['price'] < market_data['atl'] * 1.2:
            event_weights: List[float] = [0.2, 0.3, 0.5]  # Higher chance of bullish events
        else:
            event_weights: List[float] = [0.33, 0.34, 0.33]  # Equal distribution
        
        events: List[Tuple[str, str, List[str], Tuple[int, int]]] = [
            (Fore.RED, "ALERT", self._get_bearish_events(current_price, market_data), (2, 5)),
            (Fore.YELLOW, "WARN", self._get_neutral_events(current_price, market_data), (1, 3)),
            (Fore.GREEN, "INFO", self._get_bullish_events(current_price, market_data), (1, 2))
        ]
        
        # Choose event type based on weights
        event_type: int = random.choices([0, 1, 2], weights=event_weights)[0]
        color, level, messages, delay_range = events[event_type]
        message: str = random.choice(messages)
        
        # Add market-aware details
        details: List[str] = self._generate_event_details(market_data)
        detail: str = random.choice(details) if random.random() < 0.4 else ""
        
        timestamp: str = time.strftime("%H:%M:%S")
        impact: str = f" [Impact: {random.uniform(0.1, 2.0):.1f}%]" if random.random() < 0.3 else ""
        
        formatted_message: str = f"{color}[{timestamp}] [{level}] {detail}: {message}{impact}"
        formatted_message += Style.RESET_ALL
        
        return formatted_message, random.uniform(delay_range[0], delay_range[1])

    def _get_bearish_events(self, current_price: float, market_data: Dict[str, Any]) -> List[str]:
        """Generate bearish market events.

        Args:
            current_price (float): Current market price
            market_data (dict): Dictionary containing market data

        Returns:
            list: List of bearish event message strings
        """
        return [
            f"Large sell wall detected at {self.display.format_price(current_price * 1.02)}",
            f"Bearish divergence forming on 4H timeframe",
            f"Whale movement: {self.display.format_volume(market_data['volume'] * random.uniform(0.001, 0.01))} BTC",
            f"Support breach at {self.display.format_price(current_price * 0.98)}",
            f"Funding rate spike to {random.uniform(-0.2, -0.05):.3f}%",
            f"Liquidation cascade: {self.display.format_volume(market_data['volume'] * random.uniform(0.005, 0.02))}",
            f"Exchange outflow: {self.display.format_volume(market_data['volume'] * random.uniform(0.01, 0.05))}",
            f"Options gamma exposure: {self.display.format_volume(market_data['volume'] * random.uniform(0.1, 0.3))}"
        ]

    def _get_neutral_events(self, current_price: float, market_data: Dict[str, Any]) -> List[str]:
        """Generate neutral market events.

        Args:
            current_price (float): Current market price
            market_data (dict): Dictionary containing market data

        Returns:
            list: List of neutral event message strings
        """
        return [
            f"Volume {random.choice(['surge', 'decline'])} at {self.display.format_price(current_price)}",
            f"RSI divergence at {random.uniform(20, 80):.1f}",
            f"Funding imbalance: {random.uniform(-0.1, 0.1):.3f}%",
            f"OI/Volume ratio: {random.uniform(0.5, 2.0):.2f}",
            f"Unusual options flow at {self.display.format_price(current_price * random.uniform(0.9, 1.1))}",
            f"Momentum shift at {self.display.format_price(current_price)}",
            f"Volatility compression: {(market_data['volatility'] * 100):.1f}%",
            f"Technical divergence on {random.choice(['RSI', 'MACD', 'OBV'])}"
        ]

    def _get_bullish_events(self, current_price: float, market_data: Dict[str, Any]) -> List[str]:
        """Generate bullish market events.

        Args:
            current_price (float): Current market price
            market_data (dict): Dictionary containing market data

        Returns:
            list: List of bullish event message strings
        """
        return [
            f"Accumulation detected: {self.display.format_volume(market_data['volume'] * random.uniform(0.01, 0.05))}",
            f"Higher low formed at {self.display.format_price(current_price * 0.99)}",
            f"Golden cross: MA50 crosses MA200",
            f"Support forming at {self.display.format_price(current_price * 0.95)}",
            f"Institutional inflow: {self.display.format_volume(market_data['volume'] * random.uniform(0.02, 0.08))}",
            f"Funding normalization at {random.uniform(-0.01, 0.01):.3f}%",
            f"OI reset complete: {self.display.format_volume(market_data['volume'] * random.uniform(0.5, 0.8))}",
            f"Volatility breakout: {(market_data['volatility'] * 100 * random.uniform(1.2, 1.5)):.1f}%"
        ]

    def _generate_event_details(self, market_data: Dict[str, Any]) -> List[str]:
        """Generate additional event details.

        Args:
            market_data (dict): Dictionary containing market data

        Returns:
            list: List of event detail strings
        """
        return [
            f"(Vol: {self.display.format_volume(market_data['volume'] * random.uniform(0.001, 0.01))})",
            f"(OI: {self.display.format_volume(market_data['volume'] * random.uniform(0.4, 0.8))})",
            f"(Lvg: {random.uniform(2, 20):.1f}x)",
            f"(Depth: {self.display.format_volume(market_data['volume'] * random.uniform(0.01, 0.05))})",
            f"(Spread: {random.uniform(0.01, 0.1):.3f}%)",
            f"(CVD: {self.display.format_volume(market_data['volume'] * random.uniform(-0.1, 0.1))})"
        ]
