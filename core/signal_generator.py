from core.signal_analyzer import analyze_market
from core.coin_filter import is_valid_coin
from core.strategy_classifier import classify_strategy
from core.risk_evaluator import evaluate_risk
from core.risk_manager import calc_sl_tp

def generate_signals(market_data):
    signals = []
    for coin in market_data:
        symbol = coin["symbol"]
        rsi, volume, funding, change, entry = coin["rsi"], coin["volume"], coin["funding"], coin["change"], coin["price"]

        if not is_valid_coin(symbol, volume): continue
        if not analyze_market(rsi, funding, change): continue

        strategy = classify_strategy(rsi, funding)
        sl, tp = calc_sl_tp(entry)
        risk_score = evaluate_risk(rsi, volume, funding)

        signals.append({
            "symbol": symbol,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "strategy": strategy,
            "rr": round((tp - entry) / (entry - sl), 2),
            "risk": risk_score
        })
    return signals
