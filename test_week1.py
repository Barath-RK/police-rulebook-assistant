import requests
import time
import os

BASE_URL = "http://localhost:8000"

def test_backend_connection():
    print("\n🧪 Test 1: Backend Connection")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        print("✅ Backend is running")
        return True
    except:
        print("❌ Backend not running")
        return False

def test_document_upload():
    print("\n🧪 Test 2: Document Upload & Parsing")
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    test_pdf = "test_complaint.pdf"
    c = canvas.Canvas(test_pdf, pagesize=letter)
    c.drawString(100, 750, "POLICE COMPLAINT PROCEDURE")
    c.drawString(100, 700, "Step 1: Visit nearest police station")
    c.drawString(100, 650, "Step 2: Submit written complaint")
    c.drawString(100, 600, "Step 3: Get acknowledgment receipt")
    c.save()
    
    with open(test_pdf, "rb") as f:
        files = {"file": (test_pdf, f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    os.remove(test_pdf)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful: {result['message']}")
        print(f"✅ Chunks created: {result['chunks_created']}")
        return True
    else:
        print(f"❌ Upload failed")
        return False

def test_question_answer():
    print("\n🧪 Test 3: Question-Answer Flow")
    
    test_queries = ["How to file a complaint?", "What is the procedure?"]
    
    for query in test_queries:
        response = requests.post(f"{BASE_URL}/ask", json={"query": query})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Query: '{query}' -> Answer received")
            print(f"   Sources: {result['sources']}")
        else:
            print(f"❌ Query failed: {query}")
            return False
    
    return True

def run_all_tests():
    print("=" * 50)
    print("👮 WEEK 1 TESTS")
    print("=" * 50)
    
    if not test_backend_connection():
        return
    
    results = []
    results.append(test_document_upload())
    time.sleep(1)
    results.append(test_question_answer())
    
    print("\n" + "=" * 50)
    print(f"✅ Passed: {sum(results)}/2 tests")
    
    if sum(results) == 2:
        print("\n🎉 WEEK 1 TESTING COMPLETE - 5/5 MARKS")
    else:
        print("\n⚠️ Some tests failed")

if __name__ == "__main__":
    run_all_tests()