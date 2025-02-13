# Codice: Simulatore di dati ambientali e di produzione per un'azienda agricola 
# Autore: Carmelo Panepinto
# Versione: 1.0
# Ultima modifica: 13/02/2024

# Importazione librerie
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Impostazioni della simulazione
NUM_GIORNI = 365  # Numero di giorni da simulare
COLTURE = ['Grano', 'Mais', 'Soia']  # Tipologie di colture

# Generazione dati stagionali
Giorni = np.arange(1, NUM_GIORNI + 1)
mesi = (Giorni % 365) // 30  # Approssimazione dei mesi

# La temperatura è più alta in estate e più bassa in inverno
temperature = 10 + 10 * np.sin(2 * np.pi * Giorni / 365) + np.random.normal(0, 2, NUM_GIORNI)

# L'umidità è più alta in inverno e più bassa in estate
umidita = 70 - 20 * np.sin(2 * np.pi * Giorni / 365) + np.random.normal(0, 5, NUM_GIORNI)

# Le precipitazioni sono più frequenti in autunno e inverno, minori in estate
precipitazioni = np.clip(5 + 5 * np.sin(2 * np.pi * (Giorni - 60) / 365) + np.random.exponential(2, NUM_GIORNI), 0, 15)

# Le ore di luce sono più lunghe in estate e più corte in inverno
ore_luce = 8 + 4 * np.sin(2 * np.pi * (Giorni - 80) / 365)

# Creazione DataFrame per i dati ambientali
dati_ambientali = pd.DataFrame({
    'Giorno': Giorni,
    'Temperatura (°C)': temperature,
    'Umidità (%)': np.clip(umidita, 20, 100),
    'Precipitazioni (mm)': precipitazioni,
    'Ore di Luce (h)': np.clip(ore_luce, 6, 14)
})

# Generazione dati di produzione con correlazioni realistiche
raccolto = {}
tempi_crescita = {}
uso_fertilizzanti = {}
consumo_acqua = {}

for coltura in COLTURE:
    # L'uso di fertilizzanti è minore in estate e maggiore in inverno
    uso_fertilizzanti[coltura] = np.clip((50 - 10 * np.sin(2 * np.pi * Giorni / 365)) * (1 - precipitazioni / 50), 20, 60)
    
    # Il consumo d'acqua è minore con più umidità e maggiore con temperature elevate
    consumo_acqua[coltura] = np.clip((6000 - 2000 * np.sin(2 * np.pi * Giorni / 365)) * (1 - umidita / 100), 500, 10000)
    
    # Il tempo di crescita delle colture varia in base alla temperatura e alle ore di luce
    tempi_crescita[coltura] = np.clip(100 - 10 * np.sin(2 * np.pi * Giorni / 365) + np.random.uniform(-5, 5, NUM_GIORNI), 70, 120)
    
    # Il raccolto dipende da: ore di luce, umidità, temperatura, fertilizzanti e precipitazioni
    raccolto[coltura] = 80 + 4 * ore_luce + 1.5 * umidita - 2 * precipitazioni + \
                          0.7 * uso_fertilizzanti[coltura] + 2 * temperature + \
                          np.random.normal(0, 10, NUM_GIORNI)

# Creazione DataFrame per i dati
dati_produzione = pd.DataFrame({'Giorno': Giorni})
for coltura in COLTURE:
    dati_produzione[f'Raccolto {coltura} (kg)'] = raccolto[coltura]
    dati_produzione[f'Tempi Crescita {coltura} (giorni)'] = tempi_crescita[coltura]
    dati_produzione[f'Uso Fertilizzanti {coltura} (kg/ha)'] = uso_fertilizzanti[coltura]
    dati_produzione[f'Consumo Acqua {coltura} (litri)'] = consumo_acqua[coltura]

# Unione dei due DataFrame
dati_simulati = pd.merge(dati_ambientali, dati_produzione, on='Giorno')

# Salvataggio dei dati in CSV
dati_simulati.to_csv('./Simulatore/dati_simulati.csv', index=False)

print("Simulazione completata con correlazioni realistiche e raccolto variabile. I dati sono stati salvati in 'Simulatore/dati_simulati.csv'.")

