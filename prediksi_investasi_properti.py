import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset and model
file_path = 'properti_real_estate.csv'  # Path dataset
data = pd.read_csv(file_path)

model = pickle.load(open('prediksi_investasi_properti.sav', 'rb'))

# EDA Section
st.header("Analisis Data Eksplorasi (EDA)")

# Define function for stacked bar chart
def stacked_bar(variable):
    locations = data['Lokasi'].unique()
    percentages = []

    for lokasi in locations:
        counts = data[data['Lokasi'] == lokasi][variable].value_counts(normalize=True)
        percentages.append(counts)

    # Convert to DataFrame and fill missing values with 0
    dataset = pd.DataFrame(percentages, index=locations).fillna(0)

    # Plot the stacked bar chart
    dataset.plot(kind='bar', stacked=True, figsize=(10, 6), title=f"Presentase {variable} Berdasarkan Lokasi")
    plt.ylabel('Presentase')
    plt.xlabel('Lokasi')
    plt.xticks(rotation=45)
    plt.legend(title=variable, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(plt)

# Dropdown menu for EDA
st.write("Pilih variabel untuk menampilkan grafik batang bertumpuk.")
variable = st.selectbox("Variabel:", options=['Investasi', 'Properti_Type'])

# Display the EDA chart
stacked_bar(variable)

# Streamlit title
st.title('Prediksi Kelayakan Investasi Properti Real Estate di Daerah Jakarta Selatan')

# Input fields for prediction
st.header("Input Data untuk Prediksi")
lokasi = st.number_input('Input Angka Lokasi (Cilandak: 0, Jakarta Selatan: 1, Kebayoran Baru: 2, Kebayoran Lama: 3, Mampang Prapatan: 4, Pancoran: 5, Pasar Minggu: 6, Pesanggrahan: 7)', min_value=0, max_value=7, step=1)
km = st.number_input('Jumlah Kamar Mandi', min_value=0, step=1)
kt = st.number_input('Jumlah Kamar Tidur', min_value=0, step=1)
luas = st.number_input('Input Angka Kategori Luas Bangunan (0-400m2: 0, 401-800m2: 1, >800m2:2)', min_value=0, max_value=2, step=1)
tipe = st.number_input('Input Angka Tipe Properti (Apartemen: 0, Rumah: 1)', min_value=0, max_value=1, step=1)
harga = st.number_input('Input Angka Kategori Harga (0-12.500.000.000: 0, 12.500.000.001-25.000.000.000: 1, >25.000.000.000: 2)', min_value=0, max_value=2, step=1)

predict = ''

# Prediction button
if st.button('Kelayakan Investasi'):
    predict = model.predict([[lokasi, km, kt, luas, tipe, harga]])[0]
    st.write('Properti dinyatakan **', 'Layak' if predict == 'Layak' else 'Tidak Layak', '** untuk investasi.')

