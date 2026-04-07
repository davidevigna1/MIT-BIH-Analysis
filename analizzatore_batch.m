clear all; close all; clc;

cartella_progetto = pwd; 
path_file = fullfile(cartella_progetto, '*.dat');
elenco_file = dir(path_file);

if isempty(elenco_file)
    error('ERRORE: MATLAB non vede file .dat in questa cartella. Controlla l''estensione!');
end

fprintf('Inizio analisi su %d pazienti...\n', length(elenco_file));
risultati = {}; 

for i = 1:length(elenco_file)
    nome_completo = elenco_file(i).name;
    id_paziente = erase(nome_completo, '.dat'); 
    
    % LETTURA BINARIA (Formato 212)
    fid = fopen(nome_completo, 'r');
    if fid == -1, continue; end
    A = fread(fid, [3, inf], 'uint8')';
    fclose(fid);
    
    % Conversione segnale (Canale 1)
    M1 = bitshift(bitand(A(:,2), 15), 8) + A(:,1);
    ecg = M1;
    fs = 360; 
    
    [pks, locs] = findpeaks(ecg, 'MinPeakHeight', 500, 'MinPeakDistance', 150);
    
    durata_minuti = (length(ecg)/fs) / 60;
    bpm_medio = length(pks) / durata_minuti;
    
    risultati{i, 1} = id_paziente;
    risultati{i, 2} = bpm_medio;
    
    fprintf('Analizzato Paziente %s: BPM = %.1f\n', id_paziente, bpm_medio);
end

% CREAZIONE TABELLA E CSV

tabella_finale = cell2table(risultati, 'VariableNames', {'ID_Paziente', 'BPM'});
writetable(tabella_finale, 'analisi_pazienti_batch.csv');

fprintf('✅ Successo! Creato file: analisi_pazienti_batch.csv\n');