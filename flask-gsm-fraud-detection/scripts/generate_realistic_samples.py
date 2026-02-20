"""
Generate realistic-looking sample CSVs for testing.
This script will back up existing sample files (appending .bak) and create new CSVs:
- data/sample_1.csv .. sample_4.csv (10 rows each)
- data/sample_full_table.csv (100 rows)

Fields: subscriber_id, subscriber_type, registration_date, age, income, location, is_fraud, IMEI, device_switch_count

Run: python scripts/generate_realistic_samples.py
"""
from pathlib import Path
import random
import csv
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / 'data'

random.seed(42)

LOCATIONS = ['urban', 'suburban', 'rural']
SUB_TYPES = ['prepaid', 'postpaid']


def rand_imei():
    # Generate 15-digit numeric IMEI-like string; avoid leading zeros for realism
    return ''.join(str(random.randint(0, 9)) for _ in range(15))


def rand_registration_date():
    # Random date in last 2 years
    end = datetime.utcnow()
    start = end - timedelta(days=365*2)
    d = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return d.date().isoformat()


def rand_age():
    # realistic adult age distribution (18-80, skew towards 20-50)
    return int(max(18, min(80, int(random.gauss(40, 12)))))


def rand_income():
    # income skewed log-normal-ish, typical values between 8k and 120k
    return int(max(2000, min(200000, int(random.lognormvariate(10, 0.5)))))


def rand_device_switch_count():
    # Most users have 0-2 switches; a few have higher
    r = random.random()
    if r < 0.75:
        return random.randint(0, 2)
    elif r < 0.95:
        return random.randint(3, 6)
    else:
        return random.randint(7, 15)


def maybe_fraud(device_switch_count, age, income):
    # heuristic: higher switch count and lower age/income increases fraud probability
    score = 0.05
    score += max(0, (device_switch_count - 1)) * 0.08
    if age < 25:
        score += 0.05
    if income < 15000:
        score += 0.04
    return 1 if random.random() < score else 0


def write_csv(path: Path, rows, header):
    if path.exists():
        path.with_suffix(path.suffix + '.bak').write_bytes(path.read_bytes())
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)


# Generate small sample files (10 rows each)
start_id = 1001
for i in range(1, 5):
    rows = []
    for j in range(10):
        sid = start_id + (i - 1) * 10 + j
        stype = random.choice(SUB_TYPES)
        reg = rand_registration_date()
        age = rand_age()
        income = rand_income()
        loc = random.choice(LOCATIONS)
        imei = rand_imei()
        switches = rand_device_switch_count()
        is_fraud = maybe_fraud(switches, age, income)
        rows.append([sid, stype, reg, age, income, loc, is_fraud, imei, switches])
    fp = DATA_DIR / f'sample_{i}.csv'
    write_csv(fp, rows, ['subscriber_id','subscriber_type','registration_date','age','income','location','is_fraud','IMEI','device_switch_count'])

# Generate full table (100 rows) with some realistic clustering
rows = []
for k in range(100):
    sid = 2000 + k
    stype = random.choices(SUB_TYPES, weights=[0.6, 0.4])[0]
    reg = rand_registration_date()
    age = rand_age()
    income = rand_income()
    loc = random.choices(LOCATIONS, weights=[0.5, 0.3, 0.2])[0]
    imei = rand_imei()
    switches = rand_device_switch_count()
    is_fraud = maybe_fraud(switches, age, income)
    rows.append([sid, stype, reg, age, income, loc, is_fraud, imei, switches])
fp = DATA_DIR / 'sample_full_table.csv'
write_csv(fp, rows, ['subscriber_id','subscriber_type','registration_date','age','income','location','is_fraud','IMEI','device_switch_count'])

print('Generated sample files in', DATA_DIR)
