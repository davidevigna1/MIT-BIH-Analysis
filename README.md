# MIT-BIH-Analysis
This project implements a data pipeline designed to process cardiac signals from the MIT-BIH Arrhythmia Database. The goal is to demonstrate a realistic workflow for medical data management: extracting heart rate features from raw binary signals, performing clinical statistical analysis, and automating the storage into a relational database.
# 🏥 Clinical ECG Data Pipeline: MIT-BIH Analysis

2) Requirements & Setup
To run this pipeline, you need:

MATLAB: For initial signal decoding and peak detection.

Python 3.x: With pandas and mysql-connector-python libraries.

XAMPP: To host the local MySQL/MariaDB server.

Beekeeper Studio: Or any SQL client to visualize and query the data.

Dataset Installation:

Download the MIT-BIH Arrhythmia Database ZIP file from PhysioNet.

Extract the ZIP content into your project folder. Ensure the .dat and .hea files are accessible by the scripts. As shown in the reference image (image_0.png), the actual signal files are located within the x_mitdb directory.

3) How the Pipeline Works (Technical Breakdown)
This project is built on three main blocks that talk to each other to transform raw signals into actionable data:

analizzatore_batch.m (The Signal Core):

Everything starts here. This MATLAB script acts as our "translator". Since the MIT-BIH data is stored in a complex 12-bit binary format (Format 212), this script decodes the raw bits into actual voltage values. Once the signal is readable, it runs a peak-detection algorithm to find each heartbeat (R-peak). By calculating the time between these peaks across the entire recording, it derives a precise average BPM for each of the 48 patients. Upon completion, it saves the initial raw results to analisi_pazienti_batch.csv directly within the database folder, alongside the signal files.

analisi_clinica.py (The Intelligence Layer):

This is where the raw numbers get their meaning. This Python script picks up where MATLAB left off. It navigates to the database folder to read the initial results, then performs a "cleanup"—formatting IDs, removing file extensions, and structuring the data. More importantly, it applies clinical logic: it evaluates each patient's BPM and labels them as Normal, Tachycardia, or Bradycardia. It also calculates global trends, such as the population average and abnormal case percentage. The finalized data and summary reports are saved in the root project folder as data_analysis.csv and clinical_summary_report.csv respectively, ready for database ingestion and clinical review.

upload_sql.py (The Storage Engine):

The final step is making the data permanent and searchable. This script automates the database management. It connects to the MySQL server and handles the heavy lifting: it creates the hospital_db schema from scratch, sets up a table with a Primary Key and timestamps, and "pours" the Python analysis into SQL. It uses optimized batch-insertion techniques, making it efficient even if the dataset were much larger.

4) Generated Files & Outputs
analisi_pazienti_batch.csv: The raw output from the MATLAB analysis, saved alongside the original signals.

data_analysis.csv: The primary clean, structured dataset containing Patient_ID, BPM, and Status, saved in the root project folder for database upload.

clinical_summary_report.csv: An executive summary report containing global metrics (e.g., "15.4% of patients show abnormal heart rates") for medical review, also saved in the root project folder.

MySQL Database (hospital_db): A relational database containing the patients_records table, fully indexed and ready for professional queries and integration with other visualization tools (like PowerBI or Grafana).

5) Example Queries
Once the data is loaded into Beekeeper Studio, you can interact with it using SQL. Here are a few examples:

A) Filter patients with Tachycardia (BPM > 100):

SQL
SELECT ID_Paziente, BPM 
FROM patients_records 
WHERE Stato = 'Tachycardia' 
ORDER BY BPM DESC;
B) Count the distribution of clinical statuses:

SQL
SELECT Stato, COUNT(*) as Total_Patients, ROUND(AVG(BPM), 1) as Avg_BPM
FROM patients_records 
GROUP BY Stato;
C) Find patients with highly irregular values (Out of Range):

SQL
SELECT * FROM patients_records 
WHERE BPM < 50 OR BPM > 120;

