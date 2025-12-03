import pandas as pd
import numpy as np
import pickle
import asyncio
import joblib

education_mapping = {

    "unknown" : -1,

    "illiterate" : 0,

    "basic.4y" : 1,

    "basic.6y" : 2,

    "basic.9y" : 3,

    "high.school" : 4,

    "professional.course": 5,

    "university.degree": 6

}

month_mapping = {

    "jan" : 0,

    "feb" : 1,

    "mar" : 2,

    "apr" : 3,

    "may" : 4,

    "jun" : 5,

    "jul" : 6,

    "aug" : 7,

    "sep" : 8,

    "oct" : 9,

    "nov" : 10,

    "dec" : 11

}

day_mapping = {

    "mon" : 0,

    "tue" : 1,

    "wed" : 2,

    "thu" : 3,

    "fri" : 4,

    "sat" : 5,

    "sun" : 6

}

outcome_mapping = {

    "failure": -1,

    "nonexistent": 0,

    "success": 1

}

job_mapping = {
    "admin.": 0, 
    "blue-collar": 1, 
    "entrepreneur": 2, 
    "housemaid": 3, 
    "management": 4, 
    "retired": 5, 
    "self-employed": 6, 
    "services": 7, 
    "student": 8, 
    "technician": 9, 
    "unemployed": 10, 
    "unknown": 11
}

marital_mapping = {
    "divorced": 0, 
    "married": 1, 
    "single": 2, 
    "unknown": 3
}

default_mapping = {
    "no": 0, 
    "unknown": 1, 
    "yes": 2
}

housing_mapping = {
    "no": 0, 
    "unknown": 1, 
    "yes": 2
}

loan_mapping = {
    "no": 0, 
    "unknown": 1, 
    "yes": 2
}

contact_mapping = {
    "cellular": 0, 
    "telephone": 1
}

try:
    scaler = joblib.load('./models/scaler_joblib.pkl')
    gb_model = joblib.load('./models/best_LGBM_without_duration_model.pkl')
    
    print("Semua objek (scaler, encoder, model) berhasil dimuat menggunakan joblib.")
except FileNotFoundError:
    print("ERROR: Pastikan Anda menjalankan train_and_save.py terlebih dahulu.")



async def preprocessing(data_input: dict):
    new_data = pd.DataFrame([data_input])

    INPUT_COLUMNS_ORDER = [
        'age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 
        'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays', 
        'previous', 'poutcome', 'emp_var_rate', 'cons_price_idx', 'cons_conf_idx', 'euribor3m', 'nr_employed', 'balance'
    ]
    


    new_data_values = [data_input[col] for col in INPUT_COLUMNS_ORDER]
    
    new_data = pd.DataFrame([new_data_values], columns=INPUT_COLUMNS_ORDER)
    
    print(f"Kolom yang dilihat Pandas: {new_data.columns.tolist()}")
    
    new_data['job'] = new_data['job'].map(job_mapping)
    new_data['marital'] = new_data['marital'].map(marital_mapping) # Perbaikan: matital -> marital
    new_data['default'] = new_data['default'].map(default_mapping)
    new_data['housing'] = new_data['housing'].map(housing_mapping)
    new_data['loan'] = new_data['loan'].map(loan_mapping)
    new_data['contact'] = new_data['contact'].map(contact_mapping)
    new_data['education'] = new_data['education'].map(education_mapping)

    new_data['month'] = new_data['month'].map(month_mapping)
    new_data['day_of_week'] = new_data['day_of_week'].map(day_mapping)
    new_data['poutcome'] = new_data['poutcome'].map(outcome_mapping)
    
    new_data['was_contacted'] = np.where(new_data['pdays'] == 999, 0, 1)
    new_data['has_previous_contact'] = np.where(new_data['previous'] == 0, 0, 1)
    new_data.drop(columns=['pdays'], inplace=True)
    new_data.drop(columns=['balance'], inplace=True)
    new_data.drop(columns=['duration'], inplace=True)
    new_data.drop(columns=['previous'], inplace=True)
    kolom_untuk_diubah = {
    'emp_var_rate': 'emp.var.rate',
    'cons_price_idx': 'cons.price.idx',
    'cons_conf_idx' : 'cons.conf.idx',
    'nr_employed': 'nr.employed'
    }
    new_data.rename(columns=kolom_untuk_diubah, inplace=True)
    new_data = scaler.transform(new_data)
    probabilities = gb_model.predict_proba(new_data)[0][1]
    
    return probabilities

dummy_input_data = {
    'age': 35,
    'job': 'blue-collar',
    'marital': 'single',
    'education': 'tertiary', 
    'default': 'no',
    'housing': 'yes',
    'loan': 'no',
    'contact': 'cellular',
    'month': 'nov',
    'day_of_week': 'mon',
    'duration': 180,  
    'campaign': 3,
    'pdays': 999,
    'previous': 0,
    'poutcome': 'unknown', 
    'emp.var.rate': 1.0,
    'cons.price.idx': 93.9,
    'cons.conf.idx': -36.0,
    'euribor3m': 4.5,
    'nr.employed': 5180.0,
    'balance': 1500,
}

# # --- 4. Eksekusi Uji Coba ---
# # Karena fungsi adalah 'async', kita harus menjalankannya menggunakan asyncio
# print("\n--- Mulai Pengujian Fungsi Preprocessing yang Telah Diperbaiki ---")
# test_probability = asyncio.run(preprocessing(dummy_input_data))

# print(f"\n✅ Probabilitas Prediksi (Kelas Positif): {test_probability:.4f}")
# print("---------------------------------")
# print("CATATAN: Hasil ini didasarkan pada model dan scaler dummy.")
