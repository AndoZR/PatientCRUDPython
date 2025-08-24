from database import engine, SessionLocal
from models import Base, Patient, User
from auth import get_password_hash
from datetime import date

# Create tables
Base.metadata.create_all(bind=engine)

def init_database():
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users == 0:
            # Create default users
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin"),
                role="admin"
            )
            
            dokter_user = User(
                username="dokter",
                password_hash=get_password_hash("dokter"),
                role="dokter"
            )
            
            db.add(admin_user)
            db.add(dokter_user)
            db.commit()
            print("✅ Default users created successfully!")
        
        # Check if patients already exist
        existing_patients = db.query(Patient).count()
        if existing_patients == 0:
            # Create sample patients
            sample_patients = [
                Patient(
                    nama="Ahmad Rizki",
                    tanggal_lahir=date(1990, 5, 15),
                    tanggal_kunjungan=date(2024, 1, 10),
                    diagnosis="Demam berdarah",
                    tindakan="Pemberian obat dan istirahat",
                    dokter="Dr. Sarah"
                ),
                Patient(
                    nama="Siti Nurhaliza",
                    tanggal_lahir=date(1985, 8, 22),
                    tanggal_kunjungan=date(2024, 1, 12),
                    diagnosis="Hipertensi",
                    tindakan="Kontrol tekanan darah",
                    dokter="Dr. Budi"
                ),
                Patient(
                    nama="Muhammad Fajar",
                    tanggal_lahir=date(1995, 3, 8),
                    tanggal_kunjungan=date(2024, 1, 15),
                    diagnosis="Flu dan batuk",
                    tindakan="Pemberian antibiotik",
                    dokter="Dr. Sarah"
                ),
                Patient(
                    nama="Dewi Sartika",
                    tanggal_lahir=date(1988, 12, 3),
                    tanggal_kunjungan=date(2024, 1, 18),
                    diagnosis="Diabetes",
                    tindakan="Kontrol gula darah",
                    dokter="Dr. Budi"
                ),
                Patient(
                    nama="Budi Santoso",
                    tanggal_lahir=date(1975, 6, 20),
                    tanggal_kunjungan=date(2024, 1, 20),
                    diagnosis="Asma",
                    tindakan="Pemberian inhaler",
                    dokter="Dr. Sarah"
                )
            ]
            
            for patient in sample_patients:
                db.add(patient)
            
            db.commit()
            print("✅ Sample patients created successfully!")
        
        print("🎉 Database initialization completed!")
        print("\n📋 Login Credentials:")
        print("   Admin: username=admin, password=admin")
        print("   Dokter: username=dokter, password=dokter")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
