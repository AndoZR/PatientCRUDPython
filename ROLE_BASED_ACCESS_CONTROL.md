# 🔐 Role-Based Access Control (RBAC) Implementation

## 🎯 Overview

Sistem Role-Based Access Control telah diimplementasikan untuk membedakan hak akses antara **Admin** dan **Dokter**:

- **Admin**: Hanya dapat melihat data pasien (View Only)
- **Dokter**: Dapat melakukan CRUD lengkap pada data pasien

## 🔧 Implementasi Teknis

### 1. Middleware Authentication

**File:** `auth.py`

```python
def require_dokter_role(current_user: User = Depends(get_current_user_from_cookie)):
    """Dependency to require dokter role for CRUD operations"""
    if current_user.role != "dokter":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only dokter can perform this action."
        )
    return current_user
```

### 2. Endpoint Protection

**File:** `main.py`

Semua endpoint CRUD dilindungi dengan `require_dokter_role`:

```python
# Create Patient - Only Dokter
@app.post("/patients", response_class=HTMLResponse)
async def create_patient(..., current_user: User = Depends(require_dokter_role)):

# Edit Patient Form - Only Dokter  
@app.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
async def edit_patient_form(..., current_user: User = Depends(require_dokter_role)):

# Update Patient - Only Dokter
@app.post("/patients/{patient_id}/update", response_class=HTMLResponse)
async def update_patient_post(..., current_user: User = Depends(require_dokter_role)):

# Delete Patient - Only Dokter
@app.post("/patients/{patient_id}/delete", response_class=HTMLResponse)
async def delete_patient(..., current_user: User = Depends(require_dokter_role)):
```

### 3. UI Middleware

**File:** `templates/patients/list.html`

```html
<!-- Show "Tambah Pasien" button only for Dokter -->
{% if user_role == "dokter" %}
<a href="/patients/new" class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-secondary transition-colors">
    + Tambah Pasien
</a>
{% endif %}

<!-- Show Edit/Delete buttons only for Dokter -->
{% if user_role == "dokter" %}
<a href="/patients/{{ patient.id }}/edit" class="text-primary hover:text-secondary">Edit</a>
<form method="POST" action="/patients/{{ patient.id }}/delete" class="inline">
    <button type="submit" class="text-danger hover:text-red-700">Hapus</button>
</form>
{% else %}
<span class="text-gray-400">View Only</span>
{% endif %}
```

### 4. Role Display

**File:** `templates/base_auth.html`

```html
<!-- Display user role in navigation -->
<span class="text-gray-500 text-sm px-3 py-2">({{ user_role|title }})</span>
```

## 📊 Role Permissions Matrix

| Feature | Admin | Dokter |
|---------|-------|--------|
| **View Patients** | ✅ | ✅ |
| **View Dashboard** | ✅ | ✅ |
| **Add Patient** | ❌ | ✅ |
| **Edit Patient** | ❌ | ✅ |
| **Delete Patient** | ❌ | ✅ |
| **Import/Export** | ✅ | ✅ |

## 🧪 Testing Results

### Admin Access Test:
```
✅ Admin login successful!
✅ /patients/new correctly blocked for admin! (403 Forbidden)
✅ /patients/1/edit correctly blocked for admin! (403 Forbidden)
✅ Admin UI correctly hides 'Tambah Pasien' button!
✅ Admin UI correctly hides 'Edit' buttons!
```

### Dokter Access Test:
```
✅ Dokter login successful!
✅ /patients/new correctly allowed for dokter! (200 OK)
✅ Dokter UI correctly shows 'Tambah Pasien' button!
✅ Dokter UI correctly shows 'Edit' buttons!
```

## 🔐 Security Features

### 1. Server-Side Protection
- **Endpoint Level**: Semua endpoint CRUD dilindungi dengan middleware
- **HTTP 403 Forbidden**: Admin yang mencoba akses CRUD akan mendapat error 403
- **Role Validation**: Validasi role dilakukan di level dependency injection

### 2. Client-Side Protection
- **UI Hiding**: Tombol CRUD disembunyikan untuk admin
- **Role Display**: Role user ditampilkan di navigasi
- **Graceful Degradation**: Admin tetap bisa melihat data tapi tidak bisa mengubah

### 3. Error Handling
```python
# Custom error message for unauthorized access
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access denied. Only dokter can perform this action."
)
```

## 👤 User Experience

### Admin Experience:
- ✅ Dapat melihat semua data pasien
- ✅ Dapat mengakses dashboard dan laporan
- ✅ Dapat melakukan import/export data
- ❌ Tidak dapat menambah, edit, atau hapus pasien
- 🎨 UI menampilkan "View Only" untuk tombol aksi

### Dokter Experience:
- ✅ Dapat melakukan CRUD lengkap pada pasien
- ✅ Dapat mengakses semua fitur
- ✅ UI menampilkan semua tombol aksi
- 🎨 Role "Dokter" ditampilkan di navigasi

## 📋 Implementation Checklist

- ✅ **Middleware Function**: `require_dokter_role()` implemented
- ✅ **Endpoint Protection**: Semua CRUD endpoint dilindungi
- ✅ **UI Middleware**: Template menggunakan conditional rendering
- ✅ **Role Display**: Role user ditampilkan di navigasi
- ✅ **Error Handling**: Custom error messages untuk unauthorized access
- ✅ **Testing**: Comprehensive testing untuk kedua role
- ✅ **Documentation**: Dokumentasi lengkap implementasi

## 🚀 Usage Guide

### Untuk Admin:
1. Login dengan: `admin/admin`
2. Akses menu "Pasien" untuk melihat data
3. Akses "Dashboard" untuk laporan
4. Gunakan fitur import/export jika diperlukan

### Untuk Dokter:
1. Login dengan: `dokter/dokter`
2. Akses menu "Pasien" untuk CRUD lengkap
3. Klik "+ Tambah Pasien" untuk menambah data baru
4. Klik "Edit" atau "Hapus" untuk mengubah data

## 🎉 Kesimpulan

**Role-Based Access Control berhasil diimplementasikan dengan sempurna!**

- ✅ **Security**: Server-side dan client-side protection
- ✅ **UX**: Interface yang berbeda untuk setiap role
- ✅ **Testing**: Semua test berhasil
- ✅ **Documentation**: Dokumentasi lengkap

**Sistem sekarang aman dan sesuai dengan requirement!** 🔐
