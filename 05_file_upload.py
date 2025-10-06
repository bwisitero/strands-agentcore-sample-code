"""
Demo 24: File Upload and Analysis with FastAPI
Goal: Build a web interface that allows file uploads and AI-powered document analysis

Key Teaching Points:
- File upload handling with FastAPI
- Multi-format document processing (PDF, DOCX, TXT, images)
- Session-based file storage
- Document Q&A with uploaded files
- Image analysis integration
- Drag-and-drop UI interface
"""

import os
import base64
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json

from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from strands import Agent, tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable autonomous tool execution
os.environ['BYPASS_TOOL_CONSENT'] = 'true'

# Initialize FastAPI app
app = FastAPI(title="Strands File Upload & Analysis")

# Session storage: session_id -> {files: [], agent: Agent}
sessions = {}

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================================
# Document Processing Functions
# ============================================================================

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading TXT file: {str(e)}"


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return "\n\n".join(text)
    except ImportError:
        return "Error: PyPDF2 not installed. Run: uv add pypdf2"
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        from docx import Document

        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    except ImportError:
        return "Error: python-docx not installed. Run: uv add python-docx"
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"


def analyze_image_file(file_path: str) -> str:
    """Analyze image using Claude Vision (if Bedrock is configured)."""
    try:
        import boto3

        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

        # Read and encode image
        with open(file_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")

        # Determine media type
        ext = Path(file_path).suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_types.get(ext, 'image/jpeg')

        # Call Claude Vision
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": "Describe this image in detail. Include any text you see, objects, people, activities, and overall context."
                        }
                    ]
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body)
        )

        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

    except Exception as e:
        # Fallback: basic image info
        from PIL import Image
        try:
            img = Image.open(file_path)
            return f"Image file: {img.format}, Size: {img.size[0]}x{img.size[1]} pixels, Mode: {img.mode}\n\n(Note: Image analysis requires AWS Bedrock configuration. See setup instructions.)"
        except:
            return f"Image file detected. (Vision analysis unavailable: {str(e)})"


def process_uploaded_file(file_path: str, filename: str) -> Dict:
    """Process an uploaded file and extract its content."""
    ext = Path(filename).suffix.lower()

    # Extract content based on file type
    if ext == '.txt':
        content = extract_text_from_txt(file_path)
        file_type = "text"
    elif ext == '.pdf':
        content = extract_text_from_pdf(file_path)
        file_type = "pdf"
    elif ext in ['.docx', '.doc']:
        content = extract_text_from_docx(file_path)
        file_type = "document"
    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        content = analyze_image_file(file_path)
        file_type = "image"
    else:
        content = f"Unsupported file type: {ext}"
        file_type = "unknown"

    return {
        "filename": filename,
        "file_path": file_path,
        "file_type": file_type,
        "extension": ext,
        "content": content,
        "uploaded_at": datetime.now().isoformat()
    }


# ============================================================================
# Agent Tools
# ============================================================================

def get_session_files(session_id: str) -> List[Dict]:
    """Get files for a specific session."""
    if session_id in sessions:
        return sessions[session_id].get("files", [])
    return []


@tool
def list_uploaded_files(session_id: str) -> str:
    """List all files uploaded in the current session."""
    files = get_session_files(session_id)

    if not files:
        return "No files have been uploaded yet."

    file_list = []
    for i, file in enumerate(files, 1):
        file_list.append(
            f"{i}. {file['filename']} ({file['file_type']}) - "
            f"uploaded at {file['uploaded_at']}"
        )

    return "Uploaded files:\n" + "\n".join(file_list)


@tool
def get_file_content(session_id: str, filename: str) -> str:
    """Get the content of a specific uploaded file."""
    files = get_session_files(session_id)

    for file in files:
        if file['filename'].lower() == filename.lower():
            return f"Content of {filename}:\n\n{file['content']}"

    return f"File '{filename}' not found. Use list_uploaded_files to see available files."


@tool
def search_files(session_id: str, query: str) -> str:
    """Search through all uploaded files for information related to the query."""
    files = get_session_files(session_id)

    if not files:
        return "No files have been uploaded yet."

    query_lower = query.lower()
    results = []

    for file in files:
        content = file['content'].lower()
        filename = file['filename']

        # Simple keyword search
        if any(word in content for word in query_lower.split()):
            # Find relevant excerpts
            lines = file['content'].split('\n')
            relevant_lines = []
            for line in lines:
                if any(word in line.lower() for word in query_lower.split()):
                    relevant_lines.append(line.strip())

            if relevant_lines:
                excerpt = '\n'.join(relevant_lines[:10])  # First 10 matching lines
                results.append(f"From {filename}:\n{excerpt}\n")

    if not results:
        return f"No relevant information found for: {query}"

    return "\n" + "="*70 + "\n".join(results)


# ============================================================================
# API Models
# ============================================================================

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def get_upload_page():
    """Serve the file upload and chat interface."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Strands File Upload & Analysis</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 20px;
                height: calc(100vh - 40px);
            }

            .panel {
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                padding: 20px;
                display: flex;
                flex-direction: column;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                border-radius: 12px;
                margin-bottom: 20px;
                font-size: 20px;
                font-weight: bold;
            }

            /* Upload Panel */
            .upload-zone {
                border: 3px dashed #667eea;
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                margin-bottom: 20px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .upload-zone:hover {
                border-color: #764ba2;
                background: #f8f9ff;
            }

            .upload-zone.dragging {
                border-color: #764ba2;
                background: #f0f0ff;
            }

            .upload-icon {
                font-size: 48px;
                margin-bottom: 10px;
            }

            #fileInput {
                display: none;
            }

            .file-list {
                flex: 1;
                overflow-y: auto;
                margin-top: 10px;
            }

            .file-item {
                background: #f8f9fa;
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
                animation: slideIn 0.3s;
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }

            .file-icon {
                font-size: 24px;
            }

            .file-info {
                flex: 1;
            }

            .file-name {
                font-weight: 600;
                color: #333;
            }

            .file-meta {
                font-size: 12px;
                color: #666;
            }

            /* Chat Panel */
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .message {
                display: flex;
                gap: 10px;
                animation: fadeIn 0.3s;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .message.user {
                justify-content: flex-end;
            }

            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
                white-space: pre-wrap;
            }

            .message.user .message-content {
                background: #667eea;
                color: white;
            }

            .message.assistant .message-content {
                background: #f1f3f4;
                color: #333;
            }

            .chat-input-container {
                padding: 20px;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
            }

            #messageInput {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 24px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }

            #messageInput:focus {
                border-color: #667eea;
            }

            #sendButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 24px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
            }

            #sendButton:hover {
                transform: scale(1.05);
            }

            #sendButton:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }

            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: #f1f3f4;
                border-radius: 18px;
                width: 60px;
            }

            .typing-indicator.show {
                display: flex;
                align-items: center;
            }

            .typing-indicator span {
                height: 8px;
                width: 8px;
                background: #999;
                border-radius: 50%;
                display: inline-block;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }

            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }

            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }

            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                transition: transform 0.2s;
            }

            .btn:hover {
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Upload Panel -->
            <div class="panel">
                <div class="header">📁 Upload Files</div>

                <div class="upload-zone" id="uploadZone">
                    <div class="upload-icon">📤</div>
                    <div>
                        <strong>Drop files here or click to browse</strong>
                        <div style="font-size: 14px; color: #666; margin-top: 8px;">
                            Supports: PDF, DOCX, TXT, Images (PNG, JPG)
                        </div>
                    </div>
                    <input type="file" id="fileInput" multiple
                           accept=".pdf,.docx,.doc,.txt,.png,.jpg,.jpeg,.gif,.webp">
                </div>

                <div style="margin-bottom: 10px; font-weight: 600; color: #333;">
                    Uploaded Files:
                </div>
                <div class="file-list" id="fileList">
                    <div style="text-align: center; color: #999; padding: 20px;">
                        No files uploaded yet
                    </div>
                </div>
            </div>

            <!-- Chat Panel -->
            <div class="panel">
                <div class="header">💬 Chat with Your Documents</div>

                <div class="chat-messages" id="chatMessages">
                    <div class="message assistant">
                        <div class="message-content">
                            Hello! Upload your files and I'll help you analyze them.
                            I can answer questions about PDFs, documents, text files, and even describe images!
                        </div>
                    </div>
                    <div class="typing-indicator" id="typingIndicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>

                <div class="chat-input-container">
                    <input
                        type="text"
                        id="messageInput"
                        placeholder="Ask a question about your uploaded files..."
                        autocomplete="off"
                    >
                    <button id="sendButton">Send</button>
                </div>
            </div>
        </div>

        <script>
            const uploadZone = document.getElementById('uploadZone');
            const fileInput = document.getElementById('fileInput');
            const fileList = document.getElementById('fileList');
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const typingIndicator = document.getElementById('typingIndicator');
            const sessionId = 'session_' + Date.now();
            let uploadedFiles = [];

            // File upload handling
            uploadZone.addEventListener('click', () => fileInput.click());

            uploadZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadZone.classList.add('dragging');
            });

            uploadZone.addEventListener('dragleave', () => {
                uploadZone.classList.remove('dragging');
            });

            uploadZone.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadZone.classList.remove('dragging');
                const files = Array.from(e.dataTransfer.files);
                uploadFiles(files);
            });

            fileInput.addEventListener('change', (e) => {
                const files = Array.from(e.target.files);
                uploadFiles(files);
            });

            async function uploadFiles(files) {
                for (const file of files) {
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('session_id', sessionId);

                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });

                        const data = await response.json();

                        if (data.success) {
                            uploadedFiles.push(data.file_info);
                            updateFileList();
                            addMessage(`File uploaded: ${file.name}`, false);
                        } else {
                            addMessage(`Error uploading ${file.name}: ${data.error}`, false);
                        }
                    } catch (error) {
                        console.error('Upload error:', error);
                        addMessage(`Error uploading ${file.name}`, false);
                    }
                }
            }

            function updateFileList() {
                if (uploadedFiles.length === 0) {
                    fileList.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">No files uploaded yet</div>';
                    return;
                }

                const fileIcons = {
                    'pdf': '📄',
                    'document': '📝',
                    'text': '📃',
                    'image': '🖼️',
                    'unknown': '📎'
                };

                fileList.innerHTML = uploadedFiles.map(file => `
                    <div class="file-item">
                        <div class="file-icon">${fileIcons[file.file_type] || '📎'}</div>
                        <div class="file-info">
                            <div class="file-name">${file.filename}</div>
                            <div class="file-meta">${file.file_type} • ${new Date(file.uploaded_at).toLocaleTimeString()}</div>
                        </div>
                    </div>
                `).join('');
            }

            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }

            function addMessage(content, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
                const escapedContent = escapeHtml(content);
                messageDiv.innerHTML = `
                    <div class="message-content">${escapedContent}</div>
                `;
                chatMessages.insertBefore(messageDiv, typingIndicator);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                messageInput.value = '';
                sendButton.disabled = true;
                typingIndicator.classList.add('show');

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            session_id: sessionId
                        })
                    });

                    const data = await response.json();

                    if (data && data.response) {
                        addMessage(data.response, false);
                    } else {
                        addMessage('Sorry, I received an empty response.', false);
                    }
                } catch (error) {
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                    console.error('Error:', error);
                } finally {
                    typingIndicator.classList.remove('show');
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            }

            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = Form(...)):
    """Handle file upload and processing."""
    try:
        # Create session directory
        session_dir = UPLOAD_DIR / session_id
        session_dir.mkdir(exist_ok=True)

        # Save file
        file_path = session_dir / file.filename
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Process file
        file_info = process_uploaded_file(str(file_path), file.filename)

        # Store in session
        if session_id not in sessions:
            sessions[session_id] = {
                "files": [],
                "agent": create_agent(session_id),
                "created_at": datetime.now()
            }

        sessions[session_id]["files"].append(file_info)

        return JSONResponse({
            "success": True,
            "file_info": file_info,
            "message": f"File {file.filename} uploaded and processed successfully"
        })

    except Exception as e:
        print(f"Error uploading file: {e}")
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    """Handle chat messages with context of uploaded files."""
    try:
        session_id = chat_message.session_id

        # Create session if it doesn't exist
        if session_id not in sessions:
            sessions[session_id] = {
                "files": [],
                "agent": create_agent(session_id),
                "created_at": datetime.now()
            }

        # Get response from agent
        session_agent = sessions[session_id]["agent"]
        response = session_agent(chat_message.message)

        response_text = str(response) if response is not None else "I apologize, but I couldn't generate a response."

        return JSONResponse({
            "response": response_text,
            "session_id": session_id
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_sessions": len(sessions),
        "total_files": sum(len(s.get("files", [])) for s in sessions.values())
    }


# ============================================================================
# Helper Functions
# ============================================================================

def create_agent(session_id: str) -> Agent:
    """Create a new agent for a session with file analysis tools."""

    # Create session-specific tool wrappers
    @tool
    def list_files() -> str:
        """List all uploaded files in the current session."""
        return list_uploaded_files(session_id)

    @tool
    def get_file(filename: str) -> str:
        """Get the full content of a specific file by filename."""
        return get_file_content(session_id, filename)

    @tool
    def search(query: str) -> str:
        """Search through all uploaded files for relevant information."""
        return search_files(session_id, query)

    agent = Agent(
        tools=[list_files, get_file, search],
        system_prompt="""You are a helpful document analysis assistant. You help users understand
        and extract information from their uploaded files.

        When users ask questions:
        1. First, check what files are available using list_files
        2. Search across files using the search tool to find relevant information
        3. Get full file content with get_file if you need complete context
        4. Provide clear, accurate answers based on the file contents
        5. Cite which files your information comes from
        6. If the answer isn't in the uploaded files, let the user know

        You can analyze:
        - PDF documents
        - Word documents (DOCX)
        - Text files (TXT)
        - Images (with descriptions and OCR)

        Be helpful, accurate, and cite your sources!
        """
    )

    return agent


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting Strands File Upload & Analysis Server")
    print("=" * 70)
    print()
    print("📱 Open http://localhost:8000 in your browser")
    print()
    print("✨ Features:")
    print("  • Drag-and-drop file upload")
    print("  • Multi-format support (PDF, DOCX, TXT, Images)")
    print("  • AI-powered document Q&A")
    print("  • Session-based file management")
    print()
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 70)

    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
Setup Instructions:

1. Install required packages:
   uv add fastapi uvicorn python-multipart pypdf2 python-docx pillow boto3

2. (Optional) Configure AWS for image analysis:
   - Set up ~/.aws/credentials
   - Enable Claude 3 in Bedrock console
   - Images will work with basic info if Bedrock isn't configured

3. Run the server:
   uv run python 24_file_upload.py

4. Open browser:
   http://localhost:8000

5. Upload files and start asking questions!

Features:
- Drag-and-drop or click to upload files
- Automatic file processing and text extraction
- PDF text extraction
- DOCX document parsing
- Image analysis with Claude Vision (if Bedrock configured)
- Session-based file storage
- Natural language Q&A over uploaded documents
- Real-time chat interface
- Beautiful, responsive UI

Example Questions to Ask:
- "What files have I uploaded?"
- "Summarize the main points from the PDF"
- "What does the contract say about salary?"
- "Search for information about pricing"
- "What's in the image I uploaded?"
- "Compare the two documents"
- "Find all mentions of deadlines"

Production Enhancements:
- Add user authentication
- Use database for file storage (S3, etc.)
- Add file size limits and validation
- Implement virus scanning
- Add file download capability
- Support more file formats (Excel, PPT, etc.)
- Add vector search for better retrieval
- Implement caching for processed files
- Add export functionality (summaries, reports)
- Rate limiting and security headers
"""
