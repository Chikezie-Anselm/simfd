import csv, random, os
from datetime import datetime, timedelta

out_dir = r"C:\Users\HP\Desktop\simfd\flask-gsm-fraud-detection\data"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# helper
def rand_imei():
    return ''.join(str(random.randint(0,9)) for _ in range(15))

locations = ['urban','rural','suburban']

# Create full_table sample
full_path = os.path.join(out_dir, 'sample_full_table.csv')
with open(full_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['subscriber_id','IMEI','fraud_probability','classification','location','device_switch_count'])
    for i in range(1001, 1011):
        p = round(random.uniform(0.25,0.95), 3)
        cls = 'Fraud' if p>0.5 else 'Legitimate'
        writer.writerow([i, rand_imei(), p, cls, random.choice(locations), random.randint(0,10)])

# Create 4 more random small samples
for s in range(1,5):
    pth = os.path.join(out_dir, f'sample_{s}.csv')
    with open(pth, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','subscriber_type','registration_date','age','income','location','is_fraud','IMEI','device_switch_count'])
        base = datetime(2023,1,1)
        for r in range(10):
            reg = (base + timedelta(days=random.randint(0,365))).strftime('%Y-%m-%d')
            is_f = 1 if random.random()>0.7 else 0
            writer.writerow([r+1, random.choice(['prepaid','postpaid']), reg, random.randint(18,70), random.randint(15000,90000), random.choice(locations), is_f, rand_imei(), random.randint(0,8)])

print('created samples')
