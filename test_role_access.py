import requests
import json

def test_role_access():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Role-Based Access Control...")
    print("=" * 60)
    
    # Test 1: Admin access (should be restricted for CRUD)
    print("1. Testing Admin Access (should be restricted for CRUD)...")
    try:
        # Login as admin
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
        
        if response.status_code == 303:
            print("   ✅ Admin login successful!")
            cookies = response.cookies
            
            # Try to access CRUD endpoints (should fail)
            crud_endpoints = [
                "/patients/new",
                "/patients/1/edit"
            ]
            
            for endpoint in crud_endpoints:
                response = requests.get(f"{base_url}{endpoint}", cookies=cookies, allow_redirects=False)
                print(f"   Testing {endpoint}: Status {response.status_code}")
                if response.status_code == 403:
                    print(f"   ✅ {endpoint} correctly blocked for admin!")
                else:
                    print(f"   ❌ {endpoint} should be blocked for admin!")
                    
        else:
            print("   ❌ Admin login failed!")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Dokter access (should be allowed for CRUD)
    print("\n2. Testing Dokter Access (should be allowed for CRUD)...")
    try:
        # Login as dokter
        login_data = {
            'username': 'dokter',
            'password': 'dokter'
        }
        
        response = requests.post(
            f"{base_url}/login",
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            allow_redirects=False
        )
        
        if response.status_code == 303:
            print("   ✅ Dokter login successful!")
            cookies = response.cookies
            
            # Try to access CRUD endpoints (should succeed)
            crud_endpoints = [
                "/patients/new",
                "/patients/1/edit"
            ]
            
            for endpoint in crud_endpoints:
                response = requests.get(f"{base_url}{endpoint}", cookies=cookies, allow_redirects=False)
                print(f"   Testing {endpoint}: Status {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} correctly allowed for dokter!")
                else:
                    print(f"   ❌ {endpoint} should be allowed for dokter!")
                    
        else:
            print("   ❌ Dokter login failed!")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Verify UI differences
    print("\n3. Testing UI Differences...")
    try:
        # Test admin UI (should not show CRUD buttons)
        login_data = {'username': 'admin', 'password': 'admin'}
        response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        cookies = response.cookies
        
        response = requests.get(f"{base_url}/patients", cookies=cookies)
        if response.status_code == 200:
            content = response.text
            if "Tambah Pasien" not in content:
                print("   ✅ Admin UI correctly hides 'Tambah Pasien' button!")
            else:
                print("   ❌ Admin UI should hide 'Tambah Pasien' button!")
                
            if "Edit" not in content:
                print("   ✅ Admin UI correctly hides 'Edit' buttons!")
            else:
                print("   ❌ Admin UI should hide 'Edit' buttons!")
                
        # Test dokter UI (should show CRUD buttons)
        login_data = {'username': 'dokter', 'password': 'dokter'}
        response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        cookies = response.cookies
        
        response = requests.get(f"{base_url}/patients", cookies=cookies)
        if response.status_code == 200:
            content = response.text
            if "Tambah Pasien" in content:
                print("   ✅ Dokter UI correctly shows 'Tambah Pasien' button!")
            else:
                print("   ❌ Dokter UI should show 'Tambah Pasien' button!")
                
            if "Edit" in content:
                print("   ✅ Dokter UI correctly shows 'Edit' buttons!")
            else:
                print("   ❌ Dokter UI should show 'Edit' buttons!")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Role-Based Access Control Testing Completed!")

if __name__ == "__main__":
    test_role_access()
