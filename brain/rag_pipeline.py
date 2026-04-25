import json
import logging
from openai import OpenAI
from django.conf import settings
from hub.models import Job
from documents.models import Document
from .pdf_extractor import extract_text_from_pdf, split_into_chunks
from .vector_store import index_document_chunks, search_similar_chunks

# Configure logger
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def build_prompt(job_description: str, relevant_chunks: list[str]) -> str:
    '''
    Task 5B.4.2: Build the prompt combining job requirements and resume context.
    Requesting structured JSON output for easier parsing.
    '''
    context = '\n---\n'.join(relevant_chunks)
    
    prompt = f'''
    Você é um Especialista em RH técnico. Sua tarefa é analisar um currículo baseado em uma descrição de vaga.
    
    DESCRIÇÃO DA VAGA:
    {job_description}
    
    TRECHOS RELEVANTES DO CURRÍCULO:
    {context}
    
    INSTRUÇÕES:
    1. Avalie a aderência do candidato à vaga.
    2. Gere um score de 0 a 100 (onde 100 é o match perfeito).
    3. Escreva um resumo executivo de até 4 frases destacando pontos fortes e lacunas.
    
    Responda EXCLUSIVAMENTE em formato JSON estruturado como no exemplo abaixo:
    {{
        "score": 85,
        "summary": "Texto do resumo aqui..."
    }}
    '''
    return prompt

def call_llm(prompt: str) -> str:
    '''
    Task 5B.4.3: Call the LLM API (OpenAI) to get the analysis.
    '''
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {{'role': 'system', 'content': 'Você é um assistente de recrutamento imparcial e preciso.'}},
                {{'role': 'user', 'content': prompt}}
            ],
            response_format={{'type': 'json_object'}},
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f'Error calling LLM: {str(e)}')
        raise

def parse_llm_response(response_text: str) -> dict:
    '''
    Task 5B.4.4: Parse the JSON string from LLM into a dictionary.
    '''
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        logger.error('Failed to parse LLM JSON response')
        return {{'score': 0, 'summary': 'Erro ao processar análise da IA.'}}

def run_rag_analysis(document_id: int, job_id: int) -> dict:
    '''
    Task 5B.4.5: Main orchestration function for the RAG pipeline.
    Extraction -> Chunking -> Indexing -> Retrieval -> Generation.
    '''
    try:
        # 1. Fetch data from DB
        job = Job.objects.get(pk=job_id)
        doc_record = Document.objects.get(pk=document_id)
        
        # 2. Extract and Chunking (PDF processing)
        full_text = extract_text_from_pdf(doc_record.file.path)
        if not full_text:
            return {{'score': 0, 'summary': 'O arquivo PDF não contém texto legível para análise.'}}
            
        chunks = split_into_chunks(full_text)
        
        # 3. Indexing (Vector store)
        index_document_chunks(document_id, chunks)
        
        # 4. Retrieval (Semantic search)
        # We use the job description as query to find matching skills in the resume
        relevant_chunks = search_similar_chunks(job.description, document_id, n_results=5)
        
        # 5. Generation (LLM Analysis)
        prompt = build_prompt(job.description, relevant_chunks)
        raw_response = call_llm(prompt)
        
        # 6. Final Parsing
        result = parse_llm_response(raw_response)
        
        return result

    except Exception as e:
        logger.error(f'RAG Pipeline failure for doc {document_id}: {str(e)}')
        return {{'score': 0, 'summary': f'Falha no pipeline de análise: {str(e)}'}}