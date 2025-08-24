import requests
import json

def test_crud_complete():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Complete CRUD Operations...")
    print("=" * 60)
    
    # Step 1: Login first
    print("1. Logging in...")
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin'
        }
        
        response = requests.post(
            f"{base_url}/login",
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Login Status Code: {response.status_code}")
        
        if response.status_code == 303:
            print("   ✅ Login successful!")
            cookies = response.cookies
        else:
            print("   ❌ Login failed!")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Create a new patient
    print("\n2. Testing CREATE (POST /patients)...")
    try:
        patient_data = {
            'nama': 'Test CRUD Patient',
            'tanggal_lahir': '1990-01-01',
            'tanggal_kunjungan': '2024-01-25',
            'diagnosis': 'Test diagnosis',
            'tindakan': 'Test tindakan',
            'dokter': 'Dr. Test'
        }
        
        response = requests.post(
            f"{base_url}/patients",
            data=patient_data,
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 303:
            print("   ✅ Create patient successful!")
        else:
            print("   ❌ Create patient failed!")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Read/Get the created patient
    print("\n3. Testing READ (GET /api/patients)...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            created_patient = next((p for p in patients if p['nama'] == 'Test CRUD Patient'), None)
            if created_patient:
                patient_id = created_patient['id']
                print(f"   ✅ Read patient successful!")
                print(f"   Patient ID: {patient_id}")
                print(f"   Patient name: {created_patient['nama']}")
            else:
                print("   ❌ Created patient not found!")
                return
        else:
            print(f"   ❌ Read patients failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 4: Update the patient
    print(f"\n4. Testing UPDATE (POST /patients/{patient_id}/update)...")
    try:
        update_data = {
            'nama': 'Test CRUD Patient Updated',
            'tanggal_lahir': '1990-01-01',
            'tanggal_kunjungan': '2024-01-25',
            'diagnosis': 'Updated diagnosis',
            'tindakan': 'Updated tindakan',
            'dokter': 'Dr. Updated'
        }
        
        response = requests.post(
            f"{base_url}/patients/{patient_id}/update",
            data=update_data,
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 303:
            print("   ✅ Update patient successful!")
        else:
            print("   ❌ Update patient failed!")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 5: Verify update
    print(f"\n5. Verifying UPDATE...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            updated_patient = next((p for p in patients if p['id'] == patient_id), None)
            if updated_patient and updated_patient['nama'] == 'Test CRUD Patient Updated':
                print("   ✅ Update verification successful!")
                print(f"   Updated name: {updated_patient['nama']}")
            else:
                print("   ❌ Update verification failed!")
        else:
            print(f"   ❌ Verification failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 6: Delete the patient
    print(f"\n6. Testing DELETE (POST /patients/{patient_id}/delete)...")
    try:
        response = requests.post(
            f"{base_url}/patients/{patient_id}/delete",
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 303:
            print("   ✅ Delete patient successful!")
        else:
            print("   ❌ Delete patient failed!")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 7: Verify deletion
    print(f"\n7. Verifying DELETE...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            deleted_patient = next((p for p in patients if p['id'] == patient_id), None)
            if not deleted_patient:
                print("   ✅ Delete verification successful!")
                print("   Patient successfully deleted!")
            else:
                print("   ❌ Delete verification failed!")
        else:
            print(f"   ❌ Verification failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 CRUD Testing Completed!")

if __name__ == "__main__":
    test_crud_complete()
