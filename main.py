from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import List, Optional
import pandas as pd
import json

from database import engine, get_db
from models import Base, Patient, User
from schemas import PatientCreate, PatientUpdate, UserCreate, UserLogin, Token
from auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash, get_current_user_from_cookie, get_current_user_role, require_dokter_role

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistem Manajemen Pasien", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ==================== LEVEL 1: CRUD PASIEN ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/patients", response_class=HTMLResponse)
async def list_patients(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    patients = db.query(Patient).all()
    return templates.TemplateResponse("patients/list.html", {
        "request": request, 
        "patients": patients,
        "user_role": current_user.role
    })

@app.get("/patients/new", response_class=HTMLResponse)
async def new_patient_form(request: Request, current_user: User = Depends(require_dokter_role)):
    return templates.TemplateResponse("patients/new.html", {
        "request": request,
        "user_role": current_user.role
    })

@app.post("/patients", response_class=HTMLResponse)
async def create_patient(
    request: Request,
    nama: str = Form(...),
    tanggal_lahir: str = Form(...),
    tanggal_kunjungan: str = Form(...),
    diagnosis: str = Form(""),
    tindakan: str = Form(""),
    dokter: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_dokter_role)
):
    patient_data = PatientCreate(
        nama=nama,
        tanggal_lahir=datetime.strptime(tanggal_lahir, "%Y-%m-%d").date(),
        tanggal_kunjungan=datetime.strptime(tanggal_kunjungan, "%Y-%m-%d").date(),
        diagnosis=diagnosis,
        tindakan=tindakan,
        dokter=dokter
    )
    
    db_patient = Patient(**patient_data.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return RedirectResponse(url="/patients", status_code=303)

@app.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
async def edit_patient_form(request: Request, patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_dokter_role)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return templates.TemplateResponse("patients/edit.html", {
        "request": request, 
        "patient": patient,
        "user_role": current_user.role
    })

@app.put("/patients/{patient_id}", response_class=HTMLResponse)
async def update_patient(
    request: Request,
    patient_id: int,
    nama: str = Form(...),
    tanggal_lahir: str = Form(...),
    tanggal_kunjungan: str = Form(...),
    diagnosis: str = Form(""),
    tindakan: str = Form(""),
    dokter: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_dokter_role)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient.nama = nama
    patient.tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
    patient.tanggal_kunjungan = datetime.strptime(tanggal_kunjungan, "%Y-%m-%d").date()
    patient.diagnosis = diagnosis
    patient.tindakan = tindakan
    patient.dokter = dokter
    
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

# Alternative endpoint for form submission (since HTML forms don't support PUT)
@app.post("/patients/{patient_id}/update", response_class=HTMLResponse)
async def update_patient_post(
    request: Request,
    patient_id: int,
    nama: str = Form(...),
    tanggal_lahir: str = Form(...),
    tanggal_kunjungan: str = Form(...),
    diagnosis: str = Form(""),
    tindakan: str = Form(""),
    dokter: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_dokter_role)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient.nama = nama
    patient.tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d").date()
    patient.tanggal_kunjungan = datetime.strptime(tanggal_kunjungan, "%Y-%m-%d").date()
    patient.diagnosis = diagnosis
    patient.tindakan = tindakan
    patient.dokter = dokter
    
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

@app.post("/patients/{patient_id}/delete", response_class=HTMLResponse)
async def delete_patient(request: Request, patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_dokter_role)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return RedirectResponse(url="/patients", status_code=303)

# ==================== LEVEL 2: LOGIN SEDERHANA ====================

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("auth/login.html", {
            "request": request, 
            "error": "Invalid username or password"
        })
    
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response

# ==================== LEVEL 4: DASHBOARD + LAPORAN ====================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    # Get summary statistics
    total_patients = db.query(Patient).count()
    today_patients = db.query(Patient).filter(
        Patient.tanggal_kunjungan == date.today()
    ).count()
    
    # Get all patients for the table
    patients = db.query(Patient).order_by(Patient.tanggal_kunjungan.desc()).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_patients": total_patients,
        "today_patients": today_patients,
        "patients": patients,
        "user_role": current_user.role
    })

# ==================== LEVEL 5: INTEGRASI SEDERHANA ====================

@app.post("/api/import")
async def import_patients(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        patients_data = body.get("patients", [])
        
        imported_count = 0
        for patient_data in patients_data:
            patient = Patient(
                nama=patient_data["nama"],
                tanggal_lahir=datetime.strptime(patient_data["tanggal_lahir"], "%Y-%m-%d").date(),
                tanggal_kunjungan=datetime.strptime(patient_data["tanggal_kunjungan"], "%Y-%m-%d").date(),
                diagnosis=patient_data.get("diagnosis", ""),
                tindakan=patient_data.get("tindakan", ""),
                dokter=patient_data.get("dokter", "")
            )
            db.add(patient)
            imported_count += 1
        
        db.commit()
        return {"message": f"Successfully imported {imported_count} patients"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/export")
async def export_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    
    # Convert to DataFrame
    data = []
    for patient in patients:
        data.append({
            "ID": patient.id,
            "Nama": patient.nama,
            "Tanggal Lahir": patient.tanggal_lahir,
            "Tanggal Kunjungan": patient.tanggal_kunjungan,
            "Diagnosis": patient.diagnosis,
            "Tindakan": patient.tindakan,
            "Dokter": patient.dokter
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    filename = f"patients_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(f"static/exports/{filename}", index=False)
    
    return {"download_url": f"/static/exports/{filename}"}

# ==================== API ENDPOINTS ====================

@app.get("/api/patients")
async def get_patients_api(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

@app.post("/api/patients")
async def create_patient_api(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
