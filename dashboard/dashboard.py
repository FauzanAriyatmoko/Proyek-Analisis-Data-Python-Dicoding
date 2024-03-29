import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Masukan dan Mendefinisikan DataFrame
all_bike_df = pd.read_csv("dashboard/all_data.csv")

label_musim = {
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
all_bike_df['label_musim'] = all_bike_df['weathersit_day'].map(label_musim)

datetime_columns = ["dteday"]

for column in datetime_columns:
    all_bike_df[column] = pd.to_datetime(all_bike_df[column])

min_date = all_bike_df["dteday"].min()
max_date = all_bike_df["dteday"].max()

with st.sidebar:
    # Logo perusahaan
    st.image("dashboard/logo_toko.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_bike_df[(all_bike_df["dteday"] >= str(start_date)) & 
                (all_bike_df["dteday"] <= str(end_date))]

st.header('Eksplorasi Data Analis Menggunakan Bike Data Set :bicyclist::fire:')

st.subheader('Jumlah Pengguna Harian Teregistrasi dan Pengguna Kasual')
col1, col2 = st.columns(2)
with col1 :
    total_registered = main_df.registered_hour.sum()
    st.metric("Total Pengguna Teregistrasi", value=total_registered)
with col2 :
    total_casual = main_df.casual_hour.sum()
    st.metric("Total Pengguna Kasual", value=total_casual )

# Grafik 1
col1, col2 = st.columns(2)
 
with col1 :
    total_rentals_hour = all_bike_df.groupby('hr')[['registered_hour', 'casual_hour']].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(total_rentals_hour.sum(), labels=['Teregistrasi', 'Kasual'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=90)
    
    st.pyplot(plt)
with col2 :
    daily_user_counts = main_df.groupby('dteday')[['registered_day', 'casual_day']].sum().reset_index()
    plt.figure(figsize=(14, 8))
    sns.lineplot(x='dteday', y='registered_day', data=daily_user_counts, label='Teregistrasi', marker='o', markersize=6)
    sns.lineplot(x='dteday', y='casual_day', data=daily_user_counts, label='Kasual', marker='o', markersize=6)


    plt.xlabel('Tanggal')
    plt.ylabel('Banyak Pengguna Harian')
    plt.legend()
    plt.xticks(rotation=45, ha='right')

    st.pyplot(plt)

# Grafik 2
st.subheader("Rata-Rata Penyewaan Sepedah per Jam pada setiap Bulan")
rental_jam = all_bike_df.groupby('mnth_hour')['cnt_hour'].mean()

plt.figure(figsize=(10,6))
plt.bar(rental_jam.index, rental_jam.values, color='green')

plt.title('Rata - Rata Penyewaan per Jam dalam masing-masing Bulan')
plt.xlabel('Bulan ke-')
plt.ylabel('Rata - Rata Penyewaan')

st.pyplot(plt)

# Grafik 3
st.subheader("Rata-Rata Penyewaan Sepedah per Jam pada setiap Hari")
rental_jam = all_bike_df.groupby('hr')['cnt_hour'].mean()

plt.figure(figsize=(10,6))
plt.bar(rental_jam.index, rental_jam.values, color='blue')

plt.title('Rata - Rata Penyewaan per Jam dalam Hari')
plt.xlabel('Jam')
plt.ylabel('Rata - Rata Penyewaan')

st.pyplot(plt)

# Grafik 4
st.subheader("Pengaruh Kondisi Cuaca terhadap jumlah rata-rata Pernyewaan Sepedah")
avg_weather = all_bike_df.groupby('label_musim')['cnt_day'].mean().reset_index().sort_values("cnt_day")
total_rentals = avg_weather['cnt_day'].sum()
labels = avg_weather['label_musim']
sizes = avg_weather['cnt_day']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct=lambda pct: '{:.1f}%'.format(pct), startangle=90)
plt.title('Rata - Rata Penyewaan Sepeda berdasarkan Kondisi Cuaca')
plt.ylabel('')
plt.text(0, 1.2, f"Total Jumlah Rental Sepedah: {round(total_rentals, 1)}", ha='center')
print(f"Total number of bike rentals: {total_rentals}")

st.pyplot(plt)

# Grafik 5
st.subheader("Pengaruh Hari Libur tertentu terhadap Kenaikan dan Penurunan rata-rata Penyewaan setiap Harinya")
avg_holiday = all_bike_df.groupby('holiday_day')['cnt_day'].mean().reset_index().sort_values("cnt_day")

plt.figure(figsize=(8, 5))
sns.barplot(x='holiday_day', y='cnt_day', data=avg_holiday, palette='PuOr')

plt.title('Rata-rata Penyewaan Sepedah pada Hari Libur')
plt.xlabel('Hari Libur')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks([0, 1], ['Tidak Libur', 'Libur'])

st.pyplot(plt)