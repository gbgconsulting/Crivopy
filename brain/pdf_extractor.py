import fitz  # PyMuPDF
import logging
from typing import List

# Configure logger for backend tracking
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    '''
    Task 5B.2.3: Extract plain text from a PDF file using PyMuPDF.
    Task 5B.2.5: Handle image-based PDFs or empty results.
    '''
    text = ''
    try:
        # Open the PDF document
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        
        # Check if text is empty (usually means scanned image or empty PDF)
        if not text.strip():
            logger.warning(f'Potential image-based PDF detected at: {file_path}. No text extracted.')
            return ''
            
        return text

    except Exception as e:
        logger.error(f'Failed to extract text from PDF at {file_path}: {str(e)}')
        return ''

def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    '''
    Task 5B.2.4: Split text into smaller chunks with overlap for better vector search.
    This ensures semantic context is preserved between chunks.
    '''
    chunks = []
    
    if not text:
        return chunks

    # Simple sliding window chunking logic
    start = 0
    text_length = len(text)

    while start < text_length:
        # Define the end of the current chunk
        end = start + chunk_size
        
        # Extract chunk and add to list
        chunk = text[start:end]
        chunks.append(chunk.strip())
        
        # Move the start pointer for the next chunk, accounting for overlap
        start += (chunk_size - overlap)
        
        # Safety break to avoid infinite loops if parameters are misconfigured
        if chunk_size <= overlap:
            break

    # Filter out very small or empty chunks
    return [c for c in chunks if len(c) > 10]