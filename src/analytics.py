from __future__ import annotations
import pandas as pd

STAGES = ['visit', 'product_view', 'add_to_cart', 'checkout', 'purchase']


def validate_event_order(events: pd.DataFrame) -> None:
    order = {s: i for i, s in enumerate(STAGES)}
    x = events.sort_values(['session_id','event_time']).copy()
    ranks = x['event_name'].map(order)
    if ranks.isna().any():
        raise ValueError('Unknown funnel event detected')
    bad = x.assign(rank=ranks).groupby('session_id')['rank'].apply(lambda s: not s.is_monotonic_increasing)
    if bad.any():
        raise ValueError('Out-of-order funnel events detected')


def session_stage_matrix(events: pd.DataFrame) -> pd.DataFrame:
    validate_event_order(events)
    matrix = (events.assign(reached=1)
              .pivot_table(index=['session_id','user_id','device','channel'], columns='event_name', values='reached', aggfunc='max', fill_value=0)
              .reset_index())
    for stage in STAGES:
        if stage not in matrix:
            matrix[stage] = 0
        matrix[stage] = matrix[stage].astype(int)
    return matrix


def funnel_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    counts = {stage: int(matrix[stage].sum()) for stage in STAGES}
    rows = []
    start = counts['visit']
    previous = None
    for stage in STAGES:
        current = counts[stage]
        step_rate = 100.0 if previous is None else 100 * current / previous if previous else 0.0
        rows.append({
            'stage': stage,
            'sessions': current,
            'step_conversion_pct': round(step_rate, 2),
            'step_dropoff_pct': round(100 - step_rate, 2) if previous is not None else 0.0,
            'visit_to_stage_pct': round(100 * current / start, 2) if start else 0.0,
        })
        previous = current
    return pd.DataFrame(rows)


def segmented_funnel(matrix: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in {'device', 'channel'}:
        raise ValueError('dimension must be device or channel')
    rows = []
    for value, group in matrix.groupby(dimension):
        summary = funnel_summary(group)
        summary.insert(0, dimension, value)
        rows.append(summary)
    return pd.concat(rows, ignore_index=True)


def journey_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    def outcome(row: pd.Series) -> str:
        if row.purchase: return 'Purchased'
        if row.checkout: return 'Dropped after Checkout'
        if row.add_to_cart: return 'Dropped after Cart'
        if row.product_view: return 'Dropped after Product View'
        return 'Bounced after Visit'
    out = matrix.copy()
    out['journey_outcome'] = out.apply(outcome, axis=1)
    return (out.groupby('journey_outcome').size().rename('sessions').reset_index()
            .assign(session_share_pct=lambda d: (100 * d.sessions / d.sessions.sum()).round(2))
            .sort_values('sessions', ascending=False))


def friction_table(matrix: pd.DataFrame, dimension: str) -> pd.DataFrame:
    segmented = segmented_funnel(matrix, dimension)
    transitions = segmented[segmented.stage.ne('visit')].copy()
    return transitions.sort_values('step_dropoff_pct', ascending=False).reset_index(drop=True)
