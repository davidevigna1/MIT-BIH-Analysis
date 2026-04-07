# MIT-BIH-Analysis
This project implements a data pipeline designed to process cardiac signals from the MIT-BIH Arrhythmia Database. The goal is to demonstrate a realistic workflow for medical data management: extracting heart rate features from raw binary signals, performing clinical statistical analysis, and automating the storage into a relational database.
# 🏥 Clinical ECG Data Pipeline: MIT-BIH Analysis

## 1) Requirements & Setup
To run this pipeline, you need:
* **MATLAB**: For initial signal decoding and peak detection.
* **Python 3.x**: With `pandas` and `mysql-connector-python` libraries.
* **XAMPP**: To host the local MySQL/MariaDB server.
* **Beekeeper Studio**: Or any SQL client to visualize and query the data.

**Dataset Installation:**
1. Download the **MIT-BIH Arrhythmia Database** ZIP file from [PhysioNet](https://physionet.org/content/mitdb/1.0.0/).
2. Extract the ZIP content into your project folder. Ensure the `.dat` and `.hea` files are in the same directory as the scripts.

## 2) How the Pipeline Works (Technical Breakdown)
This project is built on three main blocks that transform raw signals into actionable data:

* **`analizzatore_batch.m` (The Signal Core)**:  
  Everything starts here. This MATLAB script acts as our "translator". Since the MIT-BIH data is stored in a complex 12-bit binary format (Format 212), this script decodes the raw bits into actual voltage values. Once the signal is readable, it runs a peak-detection algorithm to find each heartbeat (R-peak). By calculating the time between these peaks across the entire recording, it derives a precise average BPM for each of the 48 patients.

* **`analisys.py` (The Intelligence Layer)**:  
  This is where the raw numbers get their meaning. This Python script picks up where MATLAB left off. It reads the generated results and performs a "cleanup", formatting IDs and handling the data structure. More importantly, it applies clinical logic: it evaluates each patient's BPM and labels them as **Normal**, **Tachycardia**, or **Bradycardia**. It also calculates global trends—like the population average and the percentage of abnormal cases—to provide a clinical overview.

* **`csv_to_sql.py` (The Storage Engine)**:  
  The final step is making the data permanent and searchable. This script automates the database management using the MySQL connector. It connects to the server and handles the heavy lifting: it creates the `hospital_db` schema from scratch, sets up a table with a Primary Key and timestamps, and "pours" the Python analysis into SQL using optimized batch-insertion techniques.

## 3) Generated Files & Outputs
* **`data_analysis.csv`**: The clean, structured dataset containing `Patient_ID`, `BPM`, and `Status`. This serves as the bridge between analysis and storage.
* **`summary_report.csv`**: An executive summary report containing global metrics (e.g., "15.4% of patients show abnormal heart rates") for medical review.
* **MySQL Database (`hospital_db`)**: A fully indexed relational database ready for professional queries and integration with tools like PowerBI or Grafana.

## 4) Example Querie
Once the data is loaded into **Beekeeper Studio**, you can interact with it using SQL:

**Example: Filter patients with Tachycardia (BPM > 100):**
```sql
SELECT ID_Paziente, BPM 
FROM patients_records 
WHERE Stato = 'Tachycardia' 
ORDER BY BPM DESC;

