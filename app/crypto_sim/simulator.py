import time
import random
from colorama import Fore, Style
from typing import Dict, List, Tuple, Any
from .market_data import MarketData
from .display import DisplayUtils
from .events import MarketEvents
from .indicators import TechnicalIndicators

class MarketSimulator:
    def __init__(self) -> None:
        self.market_data: MarketData = MarketData()
        self.display: DisplayUtils = DisplayUtils()
        self.events: MarketEvents = MarketEvents()
        self.indicators: TechnicalIndicators = TechnicalIndicators()
        self.pair: str = "BTC/USD"
        self.exchange: str = "Aggregated Markets"
        self.timeframe: str = "1m"

    def print_init_banner(self, market_data: Dict[str, Any]) -> None:
        print(Fore.GREEN + Style.BRIGHT + f"""
    ╔════════════════════════════════════════════════════════════════╗
    ║                Market Analysis Dashboard              
    ║     [Market Configuration]
    ║     - Pair: {self.pair}
    ║     - Exchange: {self.exchange}
    ║     - Timeframe: {self.timeframe}
    ║     - Initial Price: {self.display.format_price(market_data['price'])}
    ║     - 24h Volume: {self.display.format_volume(market_data['volume'])}
    ║     - Market Cap: {self.display.format_volume(market_data['market_cap'])}
    ║     
    ║     [Market Context]
    ║     - 24h Change: {market_data['price_change_24h']:+.2f}%
    ║     - ATH: {self.display.format_price(market_data['ath'])}
    ║     - Volatility: {(market_data['volatility'] * 100):.1f}%
    ║     - BTC Dominance: {market_data['dominance']:.1f}%
    ║     
    ║     [Analysis Configuration]
    ║     - Technical Indicators: RSI, MACD, OBV
    ║     - Order Flow Analysis: CVD, Funding
    ║     - Market Depth: 100 levels
    ║     - Liquidation Tracker: Enabled
    ╚════════════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)

    def initialize_simulation(self) -> None:
        """Initialize simulation components"""
        print(Fore.YELLOW + "[*] Initializing market data feeds..." + Style.RESET_ALL)
        
        init_steps: List[str] = [
            "Connecting to exchange websockets...",
            "Loading historical data...",
            "Calculating baseline metrics...",
            "Initializing technical indicators...",
            "Setting up order flow analysis...",
            "Loading market depth...",
            "Initializing liquidation feeds...",
            "Syncing funding data...",
            "Setting up alert system...",
            "Calibrating volatility models..."
        ]
        
        for step in init_steps:
            print(Fore.BLUE + f"\r[*] {step}", end="")
            for i in range(101):
                print(f"\r[*] {step}: {self.display.progress_bar(i/100)}", end="")
                time.sleep(0.05)
            print()
        
        print(Fore.GREEN + "\n[+] Market feeds initialized - Starting analysis\n" + Style.RESET_ALL)
        time.sleep(2)

    def run(self) -> None:
        """Run the market simulation"""
        # Fetch initial market data
        market_data: Dict[str, Any] = self.market_data.get_market_data()
        initial_price: float = market_data['price']
        initial_volume: float = market_data['volume'] / 24  # Convert 24h volume to hourly
        base_volatility: float = market_data['volatility'] / (24 * 60)**0.5  # Scale daily vol to per-minute
        
        self.print_init_banner(market_data)
        self.initialize_simulation()
        
        start_time: float = time.time()
        current_price: float = initial_price
        current_volume: float = initial_volume
        high_price: float = current_price
        low_price: float = current_price
        
        try:
            while True:
                elapsed: float = time.time() - start_time
                
                # Simulate market movements
                price_change: float
                volume_change: float
                price_change, volume_change = self.indicators.generate_market_metrics(
                    elapsed, base_volatility, current_price, market_data
                )
                current_price *= (1 + price_change)
                current_volume *= (1 + volume_change)
                
                high_price = max(high_price, current_price)
                low_price = min(low_price, current_price)
                
                # Random market events
                if random.random() < 0.05:  # 5% chance of event
                    event: str
                    delay: float
                    event, delay = self.events.simulate_market_event(current_price, market_data)
                    print("\n" + event)
                    time.sleep(delay)
                
                # Generate technical indicators
                indicators: Dict[str, float] = self.indicators.generate_indicators(current_price, current_volume, market_data)
                indicator_bars: Dict[str, str] = self.display.format_indicators(indicators, current_price)
                
                # Basic status line
                status: str = f"""{Fore.CYAN}[{time.strftime('%H:%M:%S')}] {self.pair}: {self.display.format_price(current_price)} | 24h: {self.display.format_volume(current_volume*24)} | Δ: {price_change*100:+.2f}%{Style.RESET_ALL}"""
                print(f"\r{status}", end="")
                
                # Detailed metrics every 30 seconds
                if int(elapsed) % 30 == 0:
                    self._print_detailed_metrics(current_price, high_price, low_price, current_volume, price_change, indicator_bars)
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            total_time: float = time.time() - start_time
            self.display.print_market_summary(total_time, initial_price, current_price, low_price, high_price, current_volume)
            return

    def _print_detailed_metrics(self, current_price: float, high_price: float, low_price: float, current_volume: float, price_change: float, indicator_bars: Dict[str, str]) -> None:
        """Print detailed market metrics"""
        summary: str = f"""
{Fore.GREEN}{'='*100}
[Market Update] {self.pair} on {self.exchange}
{Fore.YELLOW}Price Action:
    Current: {self.display.format_price(current_price)} ({price_change*100:+.2f}%)
    24h High: {self.display.format_price(high_price)} | Low: {self.display.format_price(low_price)}
    24h Volume: {self.display.format_volume(current_volume*24)}
    Price Range: {((high_price/low_price)-1)*100:.1f}%
{Fore.CYAN}Technical Analysis:
    {indicator_bars['rsi']}
    {indicator_bars['macd']}
    {indicator_bars['obv']}
{Fore.MAGENTA}Order Flow:
    {indicator_bars['funding']}
    {indicator_bars['cvd']}
    {indicator_bars['oi']}
{Fore.BLUE}Market Structure:
    Trend: {random.choice(['Bullish', 'Bearish', 'Neutral'])} ({self.timeframe})
    Volatility: {random.uniform(20, 100):.1f}%
    Liquidity: {self.display.format_volume(current_volume * random.uniform(0.1, 0.3))}
    Dominance: {random.uniform(40, 60):.1f}%{Style.RESET_ALL}"""
        print(summary)
        
        # Market insights
        insights: List[Tuple[str, float]] = [
            (f"{Fore.GREEN}[✓] Strong buy wall at {self.display.format_price(current_price * 0.98)}", 0.2),
            (f"{Fore.GREEN}[✓] Accumulation detected on spot exchanges", 0.2),
            (f"{Fore.YELLOW}[!] Funding rate divergence: {random.uniform(-0.1, 0.1):.3f}%", 0.3),
            (f"{Fore.GREEN}[✓] OI/Volume ratio healthy", 0.2),
            (f"{Fore.BLUE}[i] Large options expiry approaching", 0.2),
            (f"{Fore.YELLOW}[!] Whale wallet movement: {self.display.format_volume(random.uniform(1e6, 1e7))}", 0.3),
            (f"{Fore.GREEN}[✓] Spot premium on major exchanges", 0.2),
            (f"{Fore.BLUE}[i] Institutional flow positive", 0.3)
        ]
        
        selected_insights: List[str] = []
        for insight, prob in insights:
            if random.random() < prob and len(selected_insights) < 2:
                selected_insights.append(insight)
        
        if selected_insights:
            print("\nMarket Insights:")
            for insight in selected_insights:
                print(f"  {insight}{Style.RESET_ALL}")
                time.sleep(0.5)