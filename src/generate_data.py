from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 44
N_SESSIONS = 12000
STAGES = ['visit', 'product_view', 'add_to_cart', 'checkout', 'purchase']
DEVICES = np.array(['mobile', 'desktop', 'tablet'])
CHANNELS = np.array(['organic', 'paid_search', 'social', 'email', 'referral'])


def generate_events(output_dir: str = 'data') -> pd.DataFrame:
    """Create deterministic event-level funnel data with channel/device friction patterns."""
    rng = np.random.default_rng(SEED)
    start = pd.Timestamp('2025-01-01')
    rows: list[tuple] = []
    event_id = 1

    base_progress = {
        'product_view': 0.79,
        'add_to_cart': 0.46,
        'checkout': 0.61,
        'purchase': 0.72,
    }
    device_multiplier = {'desktop': 1.05, 'mobile': 0.91, 'tablet': 0.96}
    channel_multiplier = {'organic': 1.00, 'paid_search': 0.97, 'social': 0.88, 'email': 1.08, 'referral': 1.10}

    for session_id in range(1, N_SESSIONS + 1):
        user_id = int(rng.integers(1, 7001))
        device = str(rng.choice(DEVICES, p=[0.58, 0.34, 0.08]))
        channel = str(rng.choice(CHANNELS, p=[0.30, 0.24, 0.18, 0.14, 0.14]))
        ts = start + pd.Timedelta(minutes=int(rng.integers(0, 90 * 24 * 60)))
        rows.append((event_id, session_id, user_id, ts, 'visit', device, channel))
        event_id += 1

        previous_reached = True
        for stage in STAGES[1:]:
            if not previous_reached:
                break
            p = min(base_progress[stage] * device_multiplier[device] * channel_multiplier[channel], 0.98)
            previous_reached = bool(rng.random() < p)
            if previous_reached:
                ts += pd.Timedelta(seconds=int(rng.integers(20, 900)))
                rows.append((event_id, session_id, user_id, ts, stage, device, channel))
                event_id += 1

    events = pd.DataFrame(rows, columns=['event_id','session_id','user_id','event_time','event_name','device','channel'])
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    events.to_csv(out / 'events.csv', index=False)
    return events


if __name__ == '__main__':
    e = generate_events()
    print(f'Generated {len(e):,} events across {e.session_id.nunique():,} sessions.')
