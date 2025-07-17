from core.signal_generator import generate_signals
from core.entry_checker import check_entry_conditions
from core.multi_signal_manager import mark_reference_signal
from mess_handler import send_message
from marketdata.market_snapshot import get_market_data

def run_signal_batch():
    market_data = get_market_data()
    signals = generate_signals(market_data)

    for sig in signals:
        final_signal = mark_reference_signal(sig)
        if check_entry_conditions(sig):
            msg = (
                f"📍 {sig['symbol']} | {sig['strategy']}\n"
                f"💰 Entry: {sig['entry']:,} VND\n"
                f"🛡 SL: {sig['sl']:,} | 🎯 TP: {sig['tp']:,}\n"
                f"⚖️ R:R: {sig['rr']} | {final_signal.get('note','✅ Ready')}"
            )
            send_message(msg)
