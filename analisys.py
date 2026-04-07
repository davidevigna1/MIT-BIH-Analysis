import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "mit-bih-arrhythmia-database-1.0.0" / "analisi_pazienti_batch.csv"

df = pd.read_csv(csv_path)

df['ID_Paziente'] = df['ID_Paziente'].astype(str).str.replace('.dat', '', regex=False)

def definisci_stato(bpm):
    if bpm > 100:
        return 'Tachycardia'
    elif bpm < 60:
        return 'Bradycardia'
    else:
        return 'Normal'
df['Stato'] = df['BPM'].apply(definisci_stato) 

print("\n Analysis Summary on 48 Patients")
print(df['Stato'].value_counts()) 

total_patients = len(df)
abnormal_df = df[df['Stato'] != 'Normal']
abnormal_count = len(abnormal_df)
abnormal_percentage = (abnormal_count / total_patients) * 100

bpm_min = df['BPM'].min()
bpm_max = df['BPM'].max()
bpm_mean = df['BPM'].mean()
bpm_std = df['BPM'].std()
print("======= CLINICAL DATASET SUMMARY =======")
print(f"Total Patients:        {total_patients}")
print(f"Abnormal Cases:        {abnormal_count} ({abnormal_percentage:.1f}%)")
print("-" * 40)
print(f"BPM Range:             {bpm_min:.1f} - {bpm_max:.1f}")
print(f"Population Average:    {bpm_mean:.1f} (±{bpm_std:.1f})")
print("========================================")

if not abnormal_df.empty:
    print("\nCritical Cases List:")
    print(abnormal_df[['ID_Paziente', 'BPM', 'Stato']].sort_values(by='BPM'))

df.to_csv(BASE_DIR / 'data_analysis.csv', index=False)
print("File 'data_analysis.csv' ready for SQL!")

report_data = {
    'Metric': ['Total Patients', 'Abnormal Cases', 'Abnormal %', 'Average BPM', 'Std Dev', 'Min BPM', 'Max BPM'],
    'Value': [total_patients, abnormal_count, f"{abnormal_percentage:.2f}%", round(bpm_mean, 2), round(bpm_std, 2), bpm_min, bpm_max]
}
df_report = pd.DataFrame(report_data)
df_report.to_csv(BASE_DIR / 'summary_report.csv', index=False)

print("File 'summary_report.csv' is ready!")