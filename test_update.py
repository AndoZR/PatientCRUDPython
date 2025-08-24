import requests
import json

def test_update_endpoint():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Update Patient Endpoint...")
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
    
    # Step 2: Check if patient exists
    print("\n2. Testing GET /patients to see available patients...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            if patients:
                patient_id = patients[0]['id']
                print(f"   ✅ Found patient with ID: {patient_id}")
                print(f"   Patient name: {patients[0]['nama']}")
            else:
                print("   ❌ No patients found")
                return
        else:
            print(f"   ❌ Failed to get patients: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Test the update endpoint with authentication
    print(f"\n3. Testing POST /patients/{patient_id}/update...")
    try:
        update_data = {
            'nama': 'Test Update Patient',
            'tanggal_lahir': '1990-01-01',
            'tanggal_kunjungan': '2024-01-15',
            'diagnosis': 'Test diagnosis',
            'tindakan': 'Test tindakan',
            'dokter': 'Dr. Test'
        }
        
        response = requests.post(
            f"{base_url}/patients/{patient_id}/update",
            data=update_data,
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 303:  # Redirect after successful update
            print("   ✅ Update endpoint working!")
        else:
            print("   ❌ Update endpoint failed!")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 4: Check if the patient was actually updated
    print(f"\n4. Verifying update by checking patient data...")
    try:
        response = requests.get(f"{base_url}/api/patients", cookies=cookies)
        if response.status_code == 200:
            patients = response.json()
            updated_patient = next((p for p in patients if p['id'] == patient_id), None)
            if updated_patient:
                print(f"   ✅ Patient updated successfully!")
                print(f"   New name: {updated_patient['nama']}")
            else:
                print("   ❌ Patient not found after update")
        else:
            print(f"   ❌ Failed to verify update: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_update_endpoint()
