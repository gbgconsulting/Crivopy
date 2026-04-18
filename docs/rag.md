# Análise com IA (RAG)

O módulo de análise usa **RAG (Retrieval-Augmented Generation)** para comparar o conteúdo de um currículo PDF com os requisitos de uma vaga e gerar automaticamente um resumo e uma pontuação de aderência (score de 0 a 100).

Todo o pipeline fica na app `brain`, dentro do diretório `brain/services/`.

---

## Dependências

```
pymupdf              # extração de texto de PDFs
sentence-transformers # geração de embeddings locais
chromadb             # banco vetorial persistido em disco
openai               # chamada ao LLM (GPT-4o-mini)
```

Instalar com:

```bash
pip install pymupdf sentence-transformers chromadb openai
```

Configuração necessária em `settings.py`:

```python
CHROMA_DB_PATH = BASE_DIR / 'chroma_db'
OPENAI_API_KEY = env('OPENAI_API_KEY')  # via variável de ambiente
```

---

## Fluxo do pipeline

```
Usuário clica em "Analisar com IA"
        │
        ▼
DocumentAnalysisView (POST)
        │
        ├── Cria ou atualiza Analysis com rag_status = 'processing'
        │
        ▼
run_rag_analysis(document_id, job_id)
        │
        ├── 1. extract_text_from_pdf()     → texto bruto do PDF
        ├── 2. split_into_chunks()          → lista de trechos (chunks)
        ├── 3. index_document_chunks()      → salva embeddings no ChromaDB
        ├── 4. search_similar_chunks()      → busca trechos relevantes usando a descrição da vaga como query
        ├── 5. build_prompt()               → monta o prompt com requisitos + trechos relevantes
        ├── 6. call_llm()                   → chama a API OpenAI
        └── 7. parse_llm_response()         → extrai summary e score do retorno JSON
                │
                ▼
        Salva resultado em Analysis
        rag_status = 'done'  (ou 'error' em caso de falha)
```

---

## Serviços (`brain/services/`)

### `pdf_extractor.py`

| Função | Descrição |
|---|---|
| `extract_text_from_pdf(file_path)` | Lê o PDF com PyMuPDF e retorna o texto completo como string. Retorna string vazia se o PDF for baseado em imagem (sem texto extraível). |
| `split_into_chunks(text, chunk_size=500, overlap=50)` | Divide o texto em trechos de até `chunk_size` caracteres com sobreposição de `overlap` caracteres entre chunks consecutivos. |

### `vector_store.py`

| Função | Descrição |
|---|---|
| `get_or_create_collection(collection_name)` | Retorna (ou cria) uma coleção no ChromaDB. |
| `index_document_chunks(document_id, chunks)` | Gera embeddings para cada chunk com Sentence Transformers e os adiciona ao ChromaDB com o metadado `document_id`. |
| `search_similar_chunks(query, document_id, n_results=5)` | Busca os `n_results` chunks mais similares à `query` dentro dos chunks do `document_id` informado. |
| `delete_document_chunks(document_id)` | Remove todos os chunks de um documento do ChromaDB. Chamado automaticamente ao excluir um `Document`. |

### `rag_pipeline.py`

| Função | Descrição |
|---|---|
| `build_prompt(job_description, relevant_chunks)` | Monta o prompt enviado ao LLM com os requisitos da vaga e os trechos relevantes do currículo. O prompt instrui o LLM a retornar um JSON com `summary` e `score`. |
| `call_llm(prompt)` | Chama a API OpenAI (modelo `gpt-4o-mini`) e retorna o texto gerado. |
| `parse_llm_response(response)` | Faz parse do JSON retornado pelo LLM e extrai os campos `summary` (string) e `score` (inteiro 0–100). |
| `run_rag_analysis(document_id, job_id)` | Função principal que orquestra todo o pipeline e retorna um dict com `summary` e `score`. |

---

## Models envolvidos

**`Analysis`** — armazena o resultado da análise de um documento.

Campos relevantes: `summary`, `score`, `rag_status`, `error_message`.

**`DocumentChunk`** — armazena os chunks de texto extraídos do PDF, com referência ao ID do embedding no ChromaDB.

---

## Limpeza automática

Ao excluir um `Document`, o signal `post_delete` em `documents/signals.py` chama `delete_document_chunks(document_id)` para remover os embeddings do índice ChromaDB. Isso evita acúmulo de dados órfãos em disco.

---

## Limitações conhecidas

- PDFs baseados em imagem (escaneados sem OCR) resultam em texto vazio e a análise não é possível. O sistema registra o erro em `Analysis.error_message`.
- O pipeline é executado de forma síncrona na view. Para documentos muito grandes, isso pode causar lentidão na resposta HTTP.
- O score é gerado pelo LLM e reflete a interpretação do modelo, não uma métrica determinística.
