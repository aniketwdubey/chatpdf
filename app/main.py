from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
# import ml_logic
from . import ml_logic
import os

app = FastAPI()

class Query(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask about the PDF content.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as temp_file:
        temp_file.write(await file.read())
    
    try:
        documents = ml_logic.process_pdf(file_path)
        embeddings = ml_logic.initialize_embeddings()
        vectorstore = ml_logic.create_vectorstore(documents, embeddings)
        app.state.retriever = ml_logic.setup_retriever(vectorstore)
        app.state.llm = ml_logic.initialize_llm()
        app.state.qa_chain = ml_logic.setup_qa_chain(app.state.llm, app.state.retriever)
    finally:
        os.remove(file_path)
    
    return {"message": "PDF uploaded and processed successfully"}

@app.post("/ask/")
async def ask_question(query: Query):
    if not hasattr(app.state, 'qa_chain'):
        raise HTTPException(status_code=400, detail="Please upload a PDF first")
    
    answer = ml_logic.get_answer(app.state.qa_chain, query.question)
    return {"answer": answer}