import pandas as pd
from src.generate_data import generate_events
from src.analytics import session_stage_matrix, funnel_summary, segmented_funnel, journey_summary


def data(tmp_path):
    events = generate_events(str(tmp_path))
    return events, session_stage_matrix(events)


def test_event_population_and_temporal_order(tmp_path):
    events, matrix = data(tmp_path)
    assert matrix.session_id.nunique() == 12000
    assert events.event_id.is_unique
    assert events.groupby('session_id').event_time.apply(lambda s: s.is_monotonic_increasing).all()


def test_funnel_is_monotonic(tmp_path):
    _, matrix = data(tmp_path)
    f = funnel_summary(matrix)
    assert f.sessions.is_monotonic_decreasing
    assert f.step_conversion_pct.between(0, 100).all()
    assert f.visit_to_stage_pct.between(0, 100).all()
    assert int(f.iloc[0].sessions) == 12000


def test_purchase_implies_prior_steps(tmp_path):
    _, matrix = data(tmp_path)
    purchased = matrix[matrix.purchase.eq(1)]
    assert (purchased[['visit','product_view','add_to_cart','checkout']] == 1).all().all()


def test_segmented_funnels_reconcile(tmp_path):
    _, matrix = data(tmp_path)
    for dim in ['device','channel']:
        seg = segmented_funnel(matrix, dim)
        for stage in ['visit','product_view','add_to_cart','checkout','purchase']:
            assert int(seg.loc[seg.stage.eq(stage),'sessions'].sum()) == int(matrix[stage].sum())


def test_journey_outcomes_cover_all_sessions(tmp_path):
    _, matrix = data(tmp_path)
    journeys = journey_summary(matrix)
    assert int(journeys.sessions.sum()) == len(matrix)
    assert abs(journeys.session_share_pct.sum() - 100) < 0.1
