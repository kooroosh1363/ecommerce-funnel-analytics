from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from .generate_data import generate_events
from .analytics import session_stage_matrix, funnel_summary, segmented_funnel, journey_summary, friction_table


def main() -> None:
    out = Path('outputs')
    out.mkdir(exist_ok=True)
    events = generate_events('data')
    matrix = session_stage_matrix(events)
    funnel = funnel_summary(matrix)
    by_device = segmented_funnel(matrix, 'device')
    by_channel = segmented_funnel(matrix, 'channel')
    journeys = journey_summary(matrix)
    friction_device = friction_table(matrix, 'device')
    friction_channel = friction_table(matrix, 'channel')

    funnel.to_csv(out / 'funnel_summary.csv', index=False)
    by_device.to_csv(out / 'funnel_by_device.csv', index=False)
    by_channel.to_csv(out / 'funnel_by_channel.csv', index=False)
    journeys.to_csv(out / 'journey_outcomes.csv', index=False)
    friction_device.to_csv(out / 'device_friction.csv', index=False)
    friction_channel.to_csv(out / 'channel_friction.csv', index=False)

    ax = funnel.plot(x='stage', y='sessions', kind='bar', legend=False, title='E-commerce Funnel')
    ax.set_ylabel('Sessions')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig(out / 'funnel_overview.png', dpi=160)
    plt.close()

    purchase = by_device[by_device.stage.eq('purchase')][['device','visit_to_stage_pct']].sort_values('visit_to_stage_pct')
    ax = purchase.plot(x='device', y='visit_to_stage_pct', kind='barh', legend=False, title='Visit-to-Purchase Conversion by Device')
    ax.set_xlabel('Conversion %')
    plt.tight_layout()
    plt.savefig(out / 'device_conversion.png', dpi=160)
    plt.close()

    summary = pd.Series({
        'sessions': int(matrix.session_id.nunique()),
        'users': int(matrix.user_id.nunique()),
        'purchases': int(matrix.purchase.sum()),
        'visit_to_purchase_pct': float(funnel.loc[funnel.stage.eq('purchase'),'visit_to_stage_pct'].iloc[0]),
        'largest_step_dropoff_pct': float(funnel.loc[funnel.stage.ne('visit'),'step_dropoff_pct'].max()),
    }, name='value')
    summary.to_csv(out / 'executive_summary.csv')
    print(summary)


if __name__ == '__main__':
    main()
