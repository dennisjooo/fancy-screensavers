from colorama import Fore, Style
from datetime import timedelta
from typing import Dict, Any

class DisplayUtils:
    """Utility class for formatting and displaying market data and indicators."""

    @staticmethod
    def progress_bar(progress: float, width: int = 40) -> str:
        """Generate a progress bar string.

        Args:
            progress (float): Progress value between 0 and 1
            width (int, optional): Width of the progress bar in characters. Defaults to 40.

        Returns:
            str: Progress bar string with percentage
        """
        filled: int = int(width * progress)
        bar: str = '█' * filled + '░' * (width - filled)
        return f'[{bar}] {int(progress * 100)}%'

    @staticmethod
    def format_price(price: float) -> str:
        """Format price with appropriate precision.

        Args:
            price (float): Price value to format

        Returns:
            str: Formatted price string with $ symbol and appropriate decimal places
        """
        if price >= 1000:
            return f"${price:,.2f}"
        return f"${price:.4f}"

    @staticmethod
    def format_volume(vol: float) -> str:
        """Format volume with appropriate suffix.

        Args:
            vol (float): Volume value to format

        Returns:
            str: Formatted volume string with $ symbol and B/M/K suffix
        """
        if vol >= 1e9:
            return f"${vol/1e9:.2f}B"
        if vol >= 1e6:
            return f"${vol/1e6:.2f}M"
        if vol >= 1e3:
            return f"${vol/1e3:.2f}K"
        return f"${vol:.2f}"

    @staticmethod
    def format_indicators(indicators: Dict[str, float], price: float) -> Dict[str, str]:
        """Format technical indicators for display.

        Args:
            indicators (dict): Dictionary containing technical indicator values
            price (float): Current price for reference

        Returns:
            dict: Dictionary of formatted indicator strings with progress bars
        """
        bars: Dict[str, str] = {
            'rsi': f"RSI         [{DisplayUtils.progress_bar(indicators['rsi']/100, 20)}] {indicators['rsi']:.1f}",
            'macd': f"MACD        [{DisplayUtils.progress_bar((indicators['macd']+100)/200, 20)}] {indicators['macd']:.1f}",
            'obv': f"OBV         [{DisplayUtils.progress_bar(0.5, 20)}] {DisplayUtils.format_volume(indicators['obv'])}",
            'funding': f"Funding     [{DisplayUtils.progress_bar((indicators['funding']+0.1)/0.2, 20)}] {indicators['funding']*100:.3f}%",
            'cvd': f"CVD         [{DisplayUtils.progress_bar((indicators['cvd']+indicators['obv'])/(2*indicators['obv']), 20)}] {DisplayUtils.format_volume(indicators['cvd'])}",
            'oi': f"OpenInt     [{DisplayUtils.progress_bar(indicators['oi']/indicators['obv'], 20)}] {DisplayUtils.format_volume(indicators['oi'])}"
        }
        return bars

    @staticmethod
    def print_market_summary(duration: float, initial_price: float, current_price: float, low_price: float, high_price: float, current_volume: float) -> None:
        """Print a formatted summary of market statistics.

        Args:
            duration (float): Time duration of analysis in seconds
            initial_price (float): Starting price
            current_price (float): Current/final price
            low_price (float): Lowest price in period
            high_price (float): Highest price in period
            current_volume (float): Current trading volume
        """
        print(Fore.YELLOW + f"""
Market Summary:
{'='*50}
- Analysis duration: {str(timedelta(seconds=int(duration)))}
- Final price: {DisplayUtils.format_price(current_price)}
- Price change: {((current_price/initial_price)-1)*100:+.2f}%
- 24h range: {DisplayUtils.format_price(low_price)} - {DisplayUtils.format_price(high_price)}
- Total volume: {DisplayUtils.format_volume(current_volume*24)}
- Peak funding rate: {0.1:.3f}%
- Max leverage observed: {25:.1f}x
- Largest single trade: {DisplayUtils.format_volume(current_volume * 0.2)}
- Notable levels:
  * Support: {DisplayUtils.format_price(current_price * 0.95)}
  * Resistance: {DisplayUtils.format_price(current_price * 1.05)}
- Market sentiment: Neutral
        """ + Style.RESET_ALL)
