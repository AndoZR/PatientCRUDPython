# 🏥 Sistem Manajemen Pasien

Aplikasi sistem manajemen pasien yang dibangun dengan **FastAPI**, **PostgreSQL**, **HTML**, dan **Tailwind CSS** sesuai dengan spesifikasi tes kandidat.

## 📋 Fitur yang Diimplementasikan

### ✅ Level 1 - CRUD PASIEN
- ✅ Tabel `patients` dengan kolom: id, nama, tanggal_lahir, tanggal_kunjungan, diagnosis, tindakan, dokter
- ✅ Endpoint/halaman: Tambah pasien, Lihat daftar pasien, Edit pasien, Hapus pasien
- ✅ Teknologi: FastAPI, PostgreSQL, HTML, Tailwind CSS

### ✅ Level 2 - LOGIN SEDERHANA
- ✅ Tabel `users` dengan username dan password hash
- ✅ Endpoint `/login` untuk autentikasi
- ✅ Session/token management dengan JWT
- ✅ Akses halaman pasien setelah login

### ✅ Level 3 - Role-Based Access
- ✅ Kolom `role` pada tabel users (admin, dokter)
- ✅ Hak akses berdasarkan role:
  - Dokter: boleh tambah/edit/hapus pasien
  - Admin: hanya bisa lihat daftar pasien

### ✅ Level 4 - Dashboard + Laporan
- ✅ Halaman dashboard dengan ringkasan angka (total pasien, pasien hari ini)
- ✅ Tabel detail pasien dengan semua informasi
- ✅ Filter sederhana (by tanggal kunjungan, nama)

### ✅ Level 5 - Integrasi Sederhana
- ✅ Endpoint dummy untuk import pasien dari luar (`POST /api/import`)
- ✅ Data dummy: nama pasien + tanggal kunjungan → langsung masuk DB
- ✅ Tombol Export ke Excel dari tabel laporan

## 🚀 Cara Menjalankan Aplikasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database PostgreSQL
Pastikan PostgreSQL sudah terinstall dan running. Buat database baru:
```sql
CREATE DATABASE hospital_db;
```

### 3. Konfigurasi Environment
Buat file `.env` dengan konfigurasi berikut:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/hospital_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Inisialisasi Database
```bash
python init_db.py
```

### 5. Jalankan Aplikasi
```bash
python main.py
```

Aplikasi akan berjalan di `http://localhost:8000`

## 👤 Login Credentials

### Default Users:
- **Admin**: username=`admin`, password=`admin`
- **Dokter**: username=`dokter`, password=`dokter`

## 📁 Struktur Proyek

```
Projek/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── database.py            # Database connection
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth.py                # Authentication logic
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── patients/
│   │   ├── list.html
│   │   ├── new.html
│   │   └── edit.html
│   └── auth/
│       └── login.html
└── static/               # Static files
    └── exports/          # Excel export files
```

## 🔗 API Endpoints

### Web Pages
- `GET /` - Halaman beranda
- `GET /patients` - Daftar pasien
- `GET /patients/new` - Form tambah pasien
- `POST /patients` - Tambah pasien baru
- `GET /patients/{id}/edit` - Form edit pasien
- `POST /patients/{id}` - Update pasien
- `POST /patients/{id}/delete` - Hapus pasien
- `GET /login` - Halaman login
- `POST /login` - Proses login
- `GET /logout` - Logout
- `GET /dashboard` - Dashboard dengan laporan

### API Endpoints
- `GET /api/patients` - Get semua pasien (JSON)
- `POST /api/patients` - Tambah pasien (JSON)
- `POST /api/import` - Import data pasien (JSON)
- `GET /api/export` - Export data ke Excel

## 🎯 Fitur Utama

### 1. Manajemen Pasien
- ✅ Tambah pasien baru dengan form yang user-friendly
- ✅ Lihat daftar semua pasien dalam tabel
- ✅ Edit data pasien yang sudah ada
- ✅ Hapus pasien dengan konfirmasi

### 2. Dashboard & Laporan
- ✅ Statistik real-time (total pasien, pasien hari ini)
- ✅ Tabel laporan dengan semua data pasien
- ✅ Filter berdasarkan nama dan tanggal
- ✅ Pencarian real-time

### 3. Import/Export
- ✅ Import data pasien via JSON
- ✅ Export data ke Excel
- ✅ Download file Excel otomatis

### 4. Keamanan
- ✅ Login dengan username/password
- ✅ JWT token authentication
- ✅ Role-based access control
- ✅ Password hashing dengan bcrypt

## 🎨 UI/UX Features

- ✅ **Responsive Design** - Bekerja di desktop dan mobile
- ✅ **Modern UI** - Menggunakan Tailwind CSS
- ✅ **User-Friendly** - Interface yang intuitif
- ✅ **Real-time Search** - Pencarian instan
- ✅ **Interactive Tables** - Hover effects dan sorting
- ✅ **Form Validation** - Validasi input yang baik

## 🔧 Teknologi yang Digunakan

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT + bcrypt
- **Frontend**: HTML + Tailwind CSS
- **Export**: pandas + openpyxl
- **Templates**: Jinja2

## 📊 Database Schema

### Tabel `patients`
```sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    tanggal_kunjungan DATE NOT NULL,
    diagnosis TEXT,
    tindakan TEXT,
    dokter VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Tabel `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Deployment

Untuk deployment ke production:

1. **Environment Variables**: Update semua environment variables
2. **Database**: Gunakan PostgreSQL production server
3. **Security**: Update SECRET_KEY dan gunakan HTTPS
4. **Static Files**: Serve static files dengan nginx
5. **Process Manager**: Gunakan gunicorn atau uvicorn dengan supervisor

## 📝 Catatan

- Aplikasi ini dibuat sesuai dengan spesifikasi tes kandidat
- Semua level (1-5) telah diimplementasikan
- Kode bersih, terstruktur, dan mudah dimaintain
- Dokumentasi lengkap untuk kemudahan penggunaan

---

**Dibuat dengan ❤️ menggunakan FastAPI & Tailwind CSS**
