# MIT-BIH-Analysis

## 1) Project Presentation
This project implements a data pipeline designed to process cardiac signals from the **MIT-BIH Arrhythmia Database**. The goal is to demonstrate a realistic workflow for medical data management: extracting heart rate features from raw binary signals, performing clinical statistical analysis, and automating the storage into a professional relational database. It is a practical application of signal processing and data engineering in a MedTech context.

## 2) Requirements & Setup
To run this pipeline, you need:
* **MATLAB**: For initial signal decoding and peak detection.
* **Python 3.x**: With `pandas` and `mysql-connector-python` libraries.
* **XAMPP**: To host the local MySQL/MariaDB server.
* **Beekeeper Studio**: Or any SQL client to visualize and query the data.

**Dataset Installation:**
1. Download the **MIT-BIH Arrhythmia Database** ZIP file from [PhysioNet](https://physionet.org/content/mitdb/1.0.0/).
2. Extract the ZIP content into your project folder. Ensure the `.dat` and `.hea` files are accessible by the scripts.

## 3) How the Pipeline Works (Technical Breakdown)
This project is built on three main blocks that communicate to transform raw signals into actionable data:

* **`analizzatore_batch.m` (The Signal Core)** This MATLAB script acts as the "translator". Since the MIT-BIH data is stored in a complex 12-bit binary format (**Format 212**), the script decodes the raw bits into actual voltage values. It runs a peak-detection algorithm to find each heartbeat (R-peak) and calculates the average BPM for each of the 48 patients.  
  > **Note:** This script saves the initial raw results to `analisi_pazienti_batch.csv` directly within the database subfolder, alongside the original signal files.

* **`analisys.py` (The Intelligence Layer)** This script picks up where MATLAB left off. It navigates to the data folder to read the initial results and performs a "cleanup" (formatting IDs and structuring data). It applies clinical logic to label each patient as **Normal**, **Tachycardia**, or **Bradycardia** and calculates global trends like population average.  
  > **Note:** The finalized data (`data_analysis.csv`) and the summary report (`summary_report.csv`) are saved in the **root project folder**.

* **`csv_to_sql.py` (The Storage Engine)** The final step is making the data permanent. This script automates the database management by connecting to the MySQL server, creating the `hospital_db` schema from scratch, and "pouring" the Python analysis into SQL using optimized batch-insertion techniques.

## 4) Generated Files & Outputs
* **`analisi_pazienti_batch.csv`**: Raw output from MATLAB, located in the data subfolder.
* **`data_analysis.csv`**: Primary cleaned dataset located in the root folder, ready for SQL upload.
* **`summary_report.csv`**: Executive summary report with global metrics (e.g., "15.4% abnormal cases") for medical review.
* **MySQL Database (`hospital_db`)**: A relational database containing the `patients_records` table, fully indexed and ready for professional queries.

## 5) Example Queries
Once the data is loaded into **Beekeeper Studio**, you can interact with it using SQL:

**A) Filter patients with Tachycardia (BPM > 100):**
```sql
SELECT ID_Paziente, BPM 
FROM patients_records 
WHERE Stato = 'Tachycardia' 
ORDER BY BPM DESC;

