# 🚀 Quick Start Guide

## Aplikasi Sistem Manajemen Pasien

Aplikasi ini sudah **SIAP DIGUNAKAN** dan mengimplementasikan semua level (1-5) dari spesifikasi tes kandidat.

## ⚡ Cara Menjalankan (5 Menit)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Inisialisasi Database
```bash
python init_db.py
```

### 3. Jalankan Aplikasi
```bash
python main.py
```

### 4. Buka Browser
Kunjungi: **http://localhost:8000**

## 👤 Login Credentials

- **Admin**: username=`admin`, password=`admin`
- **Dokter**: username=`dokter`, password=`dokter`

## 🎯 Fitur yang Tersedia

### ✅ Level 1 - CRUD PASIEN
- Tambah pasien baru
- Lihat daftar pasien
- Edit data pasien
- Hapus pasien

### ✅ Level 2 - LOGIN SEDERHANA
- Login dengan username/password
- Session management dengan JWT

### ✅ Level 3 - Role-Based Access
- Role admin dan dokter
- Hak akses berbeda per role

### ✅ Level 4 - Dashboard + Laporan
- Statistik real-time
- Tabel laporan pasien
- Filter dan pencarian

### ✅ Level 5 - Integrasi SederHANA
- Import data via JSON
- Export ke Excel
- API endpoints

## 🔗 Halaman Utama

- **Beranda**: http://localhost:8000
- **Daftar Pasien**: http://localhost:8000/patients
- **Dashboard**: http://localhost:8000/dashboard
- **Login**: http://localhost:8000/login

## 🧪 Testing API

Jalankan test API untuk memverifikasi semua endpoint:
```bash
python test_api.py
```

## 📊 Database

Aplikasi menggunakan SQLite sebagai database default (file: `hospital.db`).
Data demo sudah tersedia dengan 5 pasien sample.

## 🎨 UI/UX

- **Responsive Design** - Bekerja di desktop dan mobile
- **Modern UI** - Menggunakan Tailwind CSS
- **User-Friendly** - Interface yang intuitif
- **Real-time Search** - Pencarian instan

## 🔧 Teknologi

- **Backend**: FastAPI (Python)
- **Database**: SQLite (bisa diubah ke PostgreSQL)
- **Frontend**: HTML + Tailwind CSS
- **Authentication**: JWT + bcrypt

---

**Aplikasi siap digunakan! 🎉**
