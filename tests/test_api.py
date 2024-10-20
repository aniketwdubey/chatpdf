import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf_success():
    with open("tests/test.pdf", "rb") as pdf_file:
        response = client.post(
            "/upload_pdf/",
            files={"file": ("test.pdf", pdf_file, "application/pdf")}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "PDF uploaded and processed successfully"}

def test_upload_pdf_invalid_file_type():
    response = client.post(
        "/upload_pdf/",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Only PDF files are allowed"}

def test_ask_question_success():
    # First, upload a valid PDF
    with open("tests/test.pdf", "rb") as pdf_file:
        client.post(
            "/upload_pdf/",
            files={"file": ("test.pdf", pdf_file, "application/pdf")}
        )
    
    # Now, ask a question
    response = client.post("/ask/", json={"question": "What is the name of the salesman?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    
    # Now, ask an invalid question
    response = client.post("/ask/", json={"question": ""})
    assert response.status_code == 422  # Unprocessable Entity for empty question

