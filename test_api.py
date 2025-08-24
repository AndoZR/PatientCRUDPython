import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    # Test 1: Get all patients
    print("\n1. Testing GET /api/patients")
    try:
        response = requests.get(f"{BASE_URL}/api/patients")
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ Success! Found {len(patients)} patients")
            for patient in patients[:3]:  # Show first 3
                print(f"   - {patient['nama']} (ID: {patient['id']})")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Create new patient
    print("\n2. Testing POST /api/patients")
    new_patient = {
        "nama": "Test Patient",
        "tanggal_lahir": "1990-01-01",
        "tanggal_kunjungan": "2024-01-28",
        "diagnosis": "Test diagnosis",
        "tindakan": "Test treatment",
        "dokter": "Dr. Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/patients", json=new_patient)
        if response.status_code == 200:
            patient = response.json()
            print(f"✅ Success! Created patient: {patient['nama']} (ID: {patient['id']})")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Import patients
    print("\n3. Testing POST /api/import")
    import_data = {
        "patients": [
            {
                "nama": "Imported Patient 1",
                "tanggal_lahir": "1988-05-10",
                "tanggal_kunjungan": "2024-01-29",
                "diagnosis": "Imported diagnosis",
                "tindakan": "Imported treatment",
                "dokter": "Dr. Import"
            },
            {
                "nama": "Imported Patient 2",
                "tanggal_lahir": "1995-12-25",
                "tanggal_kunjungan": "2024-01-30",
                "diagnosis": "Another diagnosis",
                "tindakan": "Another treatment",
                "dokter": "Dr. Import"
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/import", json=import_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! {result['message']}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Export patients
    print("\n4. Testing GET /api/export")
    try:
        response = requests.get(f"{BASE_URL}/api/export")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Export URL: {result['download_url']}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing completed!")
    print("\n📋 Next steps:")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Try the web interface")
    print("3. Login with admin/admin or dokter/dokter")

if __name__ == "__main__":
    test_api()
