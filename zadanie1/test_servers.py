import requests
import json

def test_server(server_name, port, url):
    test_url = f"http://127.0.0.1:{port}/parse?url={url}"
    print(f"\nTesting {server_name} server: {test_url}")
    
    try:
        response = requests.get(test_url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_url = "https://dental-first.ru/catalog"
    
    print("Testing servers...")
    print("Make sure servers are running!")
    print("Run in separate terminals:")
    print("1. python thread_server.py")
    print("2. python async_server.py")
    
    input("\nPress Enter to start tests...")
    
    if test_server("Thread", 8001, test_url):
        print(" Thread server works!")
    else:
        print(" Thread server failed!")
    
    if test_server("Async", 8002, test_url):
        print(" Async server works!")
    else:
        print(" Async server failed!")
    
    print("\nChecking result files...")
    for filename in ["thread_results.txt", "async_results.txt"]:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"{filename}: {len(lines)} lines")
        except FileNotFoundError:
            print(f"{filename}: File not found (might be empty)")