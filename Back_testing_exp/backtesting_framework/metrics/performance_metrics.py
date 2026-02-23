"""
Performance Metrics
Calculates comprehensive trading performance metrics.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime


class PerformanceMetrics:
    """
    Calculate comprehensive performance metrics for backtest results.
    
    Includes:
    - Returns (total, annualized, CAGR)
    - Risk metrics (Sharpe, Sortino, max drawdown)
    - Trade statistics
    - Win rate and profit factor
    """
    
    def __init__(self, results: Dict[str, Any], risk_free_rate: float = 0.02):
        """
        Initialize metrics calculator.
        
        Args:
            results: Backtest results dictionary
            risk_free_rate: Annual risk-free rate (default 2%)
        """
        self.results = results
        self.risk_free_rate = risk_free_rate
        
        self.trades_df = pd.DataFrame(results["trades"]) if results["trades"] else pd.DataFrame()
        self.equity_df = pd.DataFrame(results["equity_curve"])
    
    def calculate_all_metrics(self) -> Dict[str, Any]:
        """Calculate all performance metrics."""
        return {
            **self.calculate_return_metrics(),
            **self.calculate_risk_metrics(),
            **self.calculate_trade_statistics(),
            **self.calculate_cost_analysis()
        }
    
    def calculate_return_metrics(self) -> Dict[str, float]:
        """Calculate return-based metrics."""
        initial = self.results["initial_capital"]
        final = self.results["final_capital"]
        
        # Total return
        total_return = ((final - initial) / initial) * 100
        
        # Calculate time period
        if len(self.equity_df) > 0:
            start_date = self.equity_df["date"].iloc[0]
            end_date = self.equity_df["date"].iloc[-1]
            days = (end_date - start_date).days
            years = days / 365.25
        else:
            years = 1.0
        
        # Annualized return (CAGR)
        if years > 0:
            cagr = (((final / initial) ** (1 / years)) - 1) * 100
        else:
            cagr = 0.0
        
        # Calculate returns series
        if len(self.equity_df) > 1:
            self.equity_df["returns"] = self.equity_df["total_equity"].pct_change()
            daily_returns = self.equity_df["returns"].dropna()
            
            avg_daily_return = daily_returns.mean()
            avg_annual_return = avg_daily_return * 252  # Annualized
        else:
            avg_daily_return = 0.0
            avg_annual_return = 0.0
        
        return {
            "total_return_pct": round(total_return, 2),
            "cagr_pct": round(cagr, 2),
            "avg_daily_return_pct": round(avg_daily_return * 100, 4),
            "avg_annual_return_pct": round(avg_annual_return * 100, 2),
            "years": round(years, 2)
        }
    
    def calculate_risk_metrics(self) -> Dict[str, float]:
        """Calculate risk-adjusted metrics."""
        if len(self.equity_df) < 2:
            return {
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
                "max_drawdown_pct": 0.0,
                "max_drawdown_duration_days": 0,
                "volatility_annual_pct": 0.0
            }
        
        # Calculate returns
        returns = self.equity_df["total_equity"].pct_change().dropna()
        
        # Volatility
        volatility_daily = returns.std()
        volatility_annual = volatility_daily * np.sqrt(252)
        
        # Sharpe Ratio
        excess_returns = returns - (self.risk_free_rate / 252)
        if volatility_daily > 0:
            sharpe = (excess_returns.mean() / volatility_daily) * np.sqrt(252)
        else:
            sharpe = 0.0
        
        # Sortino Ratio (uses only downside deviation)
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std()
            if downside_std > 0:
                sortino = (excess_returns.mean() / downside_std) * np.sqrt(252)
            else:
                sortino = 0.0
        else:
            sortino = sharpe  # No downside, use Sharpe
        
        # Max Drawdown
        equity_curve = self.equity_df["total_equity"]
        running_max = equity_curve.expanding().max()
        drawdown = (equity_curve - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Max Drawdown Duration
        dd_duration = self._calculate_drawdown_duration(equity_curve)
        
        return {
            "sharpe_ratio": round(sharpe, 2),
            "sortino_ratio": round(sortino, 2),
            "max_drawdown_pct": round(max_drawdown, 2),
            "max_drawdown_duration_days": dd_duration,
            "volatility_annual_pct": round(volatility_annual * 100, 2)
        }
    
    def _calculate_drawdown_duration(self, equity_curve: pd.Series) -> int:
        """Calculate maximum drawdown duration in days."""
        running_max = equity_curve.expanding().max()
        is_drawdown = equity_curve < running_max
        
        # Find longest consecutive drawdown period
        max_duration = 0
        current_duration = 0
        
        for in_dd in is_drawdown:
            if in_dd:
                current_duration += 1
                max_duration = max(max_duration, current_duration)
            else:
                current_duration = 0
        
        return max_duration
    
    def calculate_trade_statistics(self) -> Dict[str, Any]:
        """Calculate trade-level statistics."""
        if len(self.trades_df) == 0:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate_pct": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "largest_win": 0.0,
                "largest_loss": 0.0,
                "profit_factor": 0.0,
                "avg_holding_days": 0.0
            }
        
        total_trades = len(self.trades_df)
        
        # Winning vs losing trades
        winners = self.trades_df[self.trades_df["net_pnl"] > 0]
        losers = self.trades_df[self.trades_df["net_pnl"] < 0]
        
        winning_trades = len(winners)
        losing_trades = len(losers)
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # Win/Loss amounts
        avg_win = winners["net_pnl"].mean() if len(winners) > 0 else 0.0
        avg_loss = losers["net_pnl"].mean() if len(losers) > 0 else 0.0
        
        largest_win = winners["net_pnl"].max() if len(winners) > 0 else 0.0
        largest_loss = losers["net_pnl"].min() if len(losers) > 0 else 0.0
        
        # Profit Factor
        total_wins = winners["net_pnl"].sum() if len(winners) > 0 else 0.0
        total_losses = abs(losers["net_pnl"].sum()) if len(losers) > 0 else 0.0
        
        profit_factor = total_wins / total_losses if total_losses > 0 else 0.0
        
        # Average holding period
        avg_holding = self.trades_df["holding_days"].mean()
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate_pct": round(win_rate, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "largest_win": round(largest_win, 2),
            "largest_loss": round(largest_loss, 2),
            "profit_factor": round(profit_factor, 2),
            "avg_holding_days": round(avg_holding, 1)
        }
    
    def calculate_cost_analysis(self) -> Dict[str, float]:
        """Analyze trading costs impact."""
        if len(self.trades_df) == 0:
            return {
                "total_costs": 0.0,
                "avg_cost_per_trade": 0.0,
                "costs_pct_of_gross_pnl": 0.0,
                "spread_costs": 0.0,
                "slippage_costs": 0.0,
                "commission_costs": 0.0,
                "financing_costs": 0.0
            }
        
        # Total costs by type
        total_spread = self.trades_df["spread_cost"].sum()
        total_slippage = self.trades_df["slippage_cost"].sum()
        total_commission = self.trades_df["commission"].sum()
        total_financing = self.trades_df["financing_cost"].sum()
        total_costs = self.trades_df["total_cost"].sum()
        
        avg_cost_per_trade = total_costs / len(self.trades_df)
        
        # Costs as percentage of gross P&L
        total_gross_pnl = self.trades_df["gross_pnl"].sum()
        if total_gross_pnl > 0:
            costs_pct = (total_costs / total_gross_pnl) * 100
        else:
            costs_pct = 0.0
        
        return {
            "total_costs": round(total_costs, 2),
            "avg_cost_per_trade": round(avg_cost_per_trade, 2),
            "costs_pct_of_gross_pnl": round(costs_pct, 2),
            "spread_costs": round(total_spread, 2),
            "slippage_costs": round(total_slippage, 2),
            "commission_costs": round(total_commission, 2),
            "financing_costs": round(total_financing, 2)
        }
    
    def print_summary(self):
        """Print formatted summary of all metrics."""
        metrics = self.calculate_all_metrics()
        
        print("=" * 80)
        print("BACKTEST PERFORMANCE SUMMARY")
        print("=" * 80)
        
        print("\n📊 RETURNS:")
        print(f"   Total Return:        {metrics['total_return_pct']:>10.2f}%")
        print(f"   CAGR:                {metrics['cagr_pct']:>10.2f}%")
        print(f"   Avg Annual Return:   {metrics['avg_annual_return_pct']:>10.2f}%")
        
        print("\n⚠️  RISK METRICS:")
        print(f"   Sharpe Ratio:        {metrics['sharpe_ratio']:>10.2f}")
        print(f"   Sortino Ratio:       {metrics['sortino_ratio']:>10.2f}")
        print(f"   Max Drawdown:        {metrics['max_drawdown_pct']:>10.2f}%")
        print(f"   Volatility (Annual): {metrics['volatility_annual_pct']:>10.2f}%")
        
        print("\n📈 TRADE STATISTICS:")
        print(f"   Total Trades:        {metrics['total_trades']:>10}")
        print(f"   Win Rate:            {metrics['win_rate_pct']:>10.2f}%")
        print(f"   Profit Factor:       {metrics['profit_factor']:>10.2f}")
        print(f"   Avg Win:             ${metrics['avg_win']:>10.2f}")
        print(f"   Avg Loss:            ${metrics['avg_loss']:>10.2f}")
        print(f"   Avg Holding:         {metrics['avg_holding_days']:>10.1f} days")
        
        print("\n💰 COST ANALYSIS:")
        print(f"   Total Costs:         ${metrics['total_costs']:>10.2f}")
        print(f"   Avg Cost/Trade:      ${metrics['avg_cost_per_trade']:>10.2f}")
        print(f"   Costs % of Gross:    {metrics['costs_pct_of_gross_pnl']:>10.2f}%")
        print(f"   Spread Costs:        ${metrics['spread_costs']:>10.2f}")
        print(f"   Slippage Costs:      ${metrics['slippage_costs']:>10.2f}")
        print(f"   Commission:          ${metrics['commission_costs']:>10.2f}")
        
        print("\n" + "=" * 80)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert metrics to DataFrame."""
        metrics = self.calculate_all_metrics()
        return pd.DataFrame([metrics])
