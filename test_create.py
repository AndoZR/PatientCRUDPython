import requests
import json

def test_create_patient():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Create Patient Endpoint...")
    print("=" * 50)
    
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
        
        if response.status_code == 303:  # Redirect after successful login
            print("   ✅ Login successful!")
            # Get cookies from response
            cookies = response.cookies
        else:
            print("   ❌ Login failed!")
            return
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Test the create patient endpoint
    print("\n2. Testing POST /patients (create new patient)...")
    try:
        patient_data = {
            'nama': 'Test Patient Baru',
            'tanggal_lahir': '1995-05-15',
            'tanggal_kunjungan': '2024-01-20',
            'diagnosis': 'Test diagnosis baru',
            'tindakan': 'Test tindakan baru',
            'dokter': 'Dr. Test Baru'
        }
        
        response = requests.post(
            f"{base_url}/patients",
            data=patient_data,
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 303:  # Redirect after successful creation
            print("   ✅ Create patient endpoint working!")
        else:
            print("   ❌ Create patient endpoint failed!")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 3: Verify the patient was created
    print(f"\n3. Verifying patient creation...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            new_patient = next((p for p in patients if p['nama'] == 'Test Patient Baru'), None)
            if new_patient:
                print(f"   ✅ Patient created successfully!")
                print(f"   Patient ID: {new_patient['id']}")
                print(f"   Patient name: {new_patient['nama']}")
            else:
                print("   ❌ Patient not found after creation")
        else:
            print(f"   ❌ Failed to verify creation: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_create_patient()
