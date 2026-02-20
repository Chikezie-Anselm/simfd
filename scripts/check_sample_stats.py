import pandas as pd
import glob

files = sorted(glob.glob('flask-gsm-fraud-detection/data/sample*.csv'))
if not files:
    print('No sample files found')
    raise SystemExit(0)

for f in files:
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print(f'Failed to read {f}: {e}')
        continue
    total = len(df)
    fp_exists = 'fraud_probability' in df.columns
    pred_exists = 'predicted_fraud' in df.columns
    is_exists = 'is_fraud' in df.columns
    avg_prob = df['fraud_probability'].mean() if fp_exists else None
    pred_sum = int(df['predicted_fraud'].sum()) if pred_exists else None
    is_sum = int(df['is_fraud'].sum()) if is_exists else None
    mismatches = None
    if pred_exists and is_exists:
        mismatches = (df['predicted_fraud'].astype(int) != df['is_fraud'].astype(int)).sum()
    print('FILE:', f)
    print('  total=', total)
    print('  fraud_probability present=', fp_exists, 'avg_prob=', avg_prob)
    print('  predicted_fraud present=', pred_exists, 'sum=', pred_sum)
    print('  is_fraud present=', is_exists, 'sum=', is_sum)
    if mismatches is not None:
        print('  predicted != actual mismatches=', mismatches)
        if mismatches > 0:
            print('  Examples (first 5 mismatches):')
            mm = df[df['predicted_fraud'].astype(int) != df['is_fraud'].astype(int)].head(5)
            print(mm[['subscriber_id','is_fraud','fraud_probability','predicted_fraud']].to_string(index=False))
    print()
