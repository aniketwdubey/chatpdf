# ChatPDF

ChatPDF is a web tool that allows users to upload PDF documents and interact with an AI assistant to ask questions about their content. Built with FastAPI for the backend and Streamlit for the frontend, it leverages machine learning libraries for efficient PDF processing and analysis.

## Features

- **PDF Upload**: Users can upload PDF files for processing.
- **AI Interaction**: Ask questions about the content of the uploaded PDFs.
- **Machine Learning Integration**: Utilizes advanced machine learning models for document processing and question answering.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Machine Learning**: Langchain, Hugging Face Transformers
- **Vector Store**: FAISS for efficient similarity search

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/chatpdf.git
   cd chatpdf
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   Create a `.env` file in the root directory and add your Hugging Face API token:

   ```plaintext
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```

## Usage

1. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Open the Streamlit app in another terminal:

   ```bash
   streamlit run app/streamlit_app.py
   ```

3. Navigate to `http://localhost:8501` in your web browser to access the application.

## API Endpoints

- **GET /**: Returns a welcome message.
- **POST /upload_pdf/**: Uploads a PDF file for processing.
  - **Request**: Multipart form data with the PDF file.
  - **Response**: Success message upon successful upload and processing.
  
- **POST /ask/**: Asks a question about the uploaded PDF.
  - **Request**: JSON body with the question.
  - **Response**: The answer to the question based on the PDF content.

## Testing

To run the tests, use:
