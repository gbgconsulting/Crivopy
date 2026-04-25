# agents/hr_agent.py
#
# Agente de IA especializado em Recrutamento e Seleção — Crivopy
#
# Implementado com LangChain 1.0 usando create_agent (API estável, out/2025).
# O agente acessa o banco de dados SQLite do Django diretamente via tools,
# com validação de ownership em cada consulta.
#
# Referência: https://docs.langchain.com/oss/python/langchain/agents
# Referência: https://docs.langchain.com/oss/python/langchain/tools

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Você é um especialista sênior em Recrutamento e Seleção com profundo
conhecimento em análise de perfis, triagem de currículos e estratégias de atração de talentos.

Seu papel é auxiliar recrutadores a tomar decisões mais inteligentes sobre os candidatos
de uma vaga específica, fornecendo análises, comparações e recomendações estratégicas com
base nos dados reais do sistema.

Diretrizes obrigatórias:
- Responda SEMPRE em português brasileiro, com linguagem profissional e objetiva.
- Baseie suas análises EXCLUSIVAMENTE nos dados retornados pelas ferramentas disponíveis.
- NUNCA invente candidatos, scores, nomes ou informações que não estejam nos dados.
- Quando os dados forem insuficientes para uma análise, informe isso claramente.
- Use as ferramentas quantas vezes forem necessárias para compor uma resposta completa.
- Ao comparar candidatos, cite nomes e scores de forma objetiva.
- Quando identificar lacunas na base de candidatos em relação aos requisitos da vaga, aponte-as.

Você tem acesso às seguintes ferramentas para consultar os dados da vaga atual:
- list_candidates: lista todos os candidatos com status e score
- get_candidate_detail: detalhes completos de um candidato específico
- get_job_summary: resumo da vaga com requisitos e estatísticas gerais
- get_top_candidates: ranking dos candidatos com maiores scores
- get_candidates_by_status: candidatos filtrados por status de triagem
"""

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------


def _get_job_model():
    from hub.models import Job  # noqa: PLC0415
    return Job


def _get_document_model():
    from documents.models import Document  # noqa: PLC0415
    return Document


def _get_analysis_model():
    from brain.models import Analysis  # noqa: PLC0415
    return Analysis


def _validate_job_ownership(job_id: int, user_id: int) -> Any | None:
    '''Retorna o Job se pertencer ao user_id, None caso contrário.'''
    Job = _get_job_model()
    try:
        return Job.objects.get(id=job_id, user_id=user_id)
    except Job.DoesNotExist:
        return None


def _format_candidate_row(doc, analysis=None) -> str:
    '''Formata uma linha de candidato para exibição em texto.'''
    score_str = f'Score RAG: {analysis.score}/100' if analysis and analysis.score is not None else 'Sem análise RAG'
    status_labels = {
        'pending': 'Pendente',
        'reviewing': 'Em análise',
        'approved': 'Aprovado',
        'rejected': 'Reprovado',
    }
    status_str = status_labels.get(doc.status, doc.status)
    email_str = f' | {doc.candidate_email}' if doc.candidate_email else ''
    return f'- {doc.candidate_name}{email_str} | Status: {status_str} | {score_str}'


# ---------------------------------------------------------------------------
# Tools — todas são read-only e validam ownership via job_id + user_id
# ---------------------------------------------------------------------------


@tool
def list_candidates(job_id: int, user_id: int, status_filter: str = '') -> str:
    '''Lista todos os candidatos de uma vaga com nome, e-mail, status e score RAG.

    Args:
        job_id: ID da vaga a ser consultada.
        user_id: ID do usuário autenticado (validação de ownership).
        status_filter: Filtro opcional de status. Valores aceitos: pending,
            reviewing, approved, rejected. Deixe vazio para listar todos.
    '''
    try:
        job = _validate_job_ownership(job_id, user_id)
        if not job:
            return 'Vaga não encontrada ou sem permissão de acesso.'

        Document = _get_document_model()
        Analysis = _get_analysis_model()

        docs = Document.objects.filter(job_id=job_id)
        if status_filter:
            docs = docs.filter(status=status_filter)

        if not docs.exists():
            filter_msg = f' com status "{status_filter}"' if status_filter else ''
            return f'Nenhum candidato encontrado para a vaga "{job.title}"{filter_msg}.'

        analyses = {
            a.document_id: a
            for a in Analysis.objects.filter(document__job_id=job_id, rag_status='done')
        }

        lines = [f'Candidatos da vaga "{job.title}" ({docs.count()} encontrado(s)):\n']
        for doc in docs.order_by('-created_at'):
            lines.append(_format_candidate_row(doc, analyses.get(doc.id)))

        return '\n'.join(lines)
    except Exception as exc:
        logger.error('list_candidates error: %s', exc)
        return 'Não foi possível listar os candidatos. Tente novamente.'


@tool
def get_candidate_detail(document_id: int, job_id: int, user_id: int) -> str:
    '''Retorna os detalhes completos de um candidato específico, incluindo notas,
    score RAG e resumo da análise de aderência.

    Args:
        document_id: ID do documento (currículo) do candidato.
        job_id: ID da vaga à qual o candidato pertence.
        user_id: ID do usuário autenticado (validação de ownership).
    '''
    try:
        job = _validate_job_ownership(job_id, user_id)
        if not job:
            return 'Vaga não encontrada ou sem permissão de acesso.'

        Document = _get_document_model()
        Analysis = _get_analysis_model()

        try:
            doc = Document.objects.get(id=document_id, job_id=job_id)
        except Document.DoesNotExist:
            return 'Candidato não encontrado para esta vaga.'

        status_labels = {
            'pending': 'Pendente',
            'reviewing': 'Em análise',
            'approved': 'Aprovado',
            'rejected': 'Reprovado',
        }

        lines = [
            f'Candidato: {doc.candidate_name}',
            f'E-mail: {doc.candidate_email or "Não informado"}',
            f'Status: {status_labels.get(doc.status, doc.status)}',
            f'Enviado em: {doc.created_at.strftime("%d/%m/%Y")}',
        ]

        if doc.notes:
            lines.append(f'Notas do recrutador: {doc.notes}')

        analysis = Analysis.objects.filter(
            document_id=document_id, rag_status='done'
        ).first()

        if analysis:
            lines.append(f'\nAnálise de IA (Score de Aderência: {analysis.score}/100):')
            lines.append(analysis.summary or 'Resumo não disponível.')
        else:
            lines.append('\nAnálise de IA: ainda não realizada para este candidato.')

        return '\n'.join(lines)
    except Exception as exc:
        logger.error('get_candidate_detail error: %s', exc)
        return 'Não foi possível obter os detalhes do candidato. Tente novamente.'


@tool
def get_job_summary(job_id: int, user_id: int) -> str:
    '''Retorna um resumo completo da vaga: título, descrição, requisitos,
    total de candidatos por status e score médio dos candidatos com análise RAG.

    Args:
        job_id: ID da vaga a ser consultada.
        user_id: ID do usuário autenticado (validação de ownership).
    '''
    try:
        job = _validate_job_ownership(job_id, user_id)
        if not job:
            return 'Vaga não encontrada ou sem permissão de acesso.'

        Document = _get_document_model()
        Analysis = _get_analysis_model()

        status_labels = {
            'pending': 'Pendente',
            'reviewing': 'Em análise',
            'approved': 'Aprovado',
            'rejected': 'Reprovado',
        }
        job_status_labels = {
            'active': 'Ativa',
            'paused': 'Pausada',
            'archived': 'Arquivada',
        }

        total = Document.objects.filter(job_id=job_id).count()
        by_status = {}
        for status_key, status_label in status_labels.items():
            count = Document.objects.filter(job_id=job_id, status=status_key).count()
            if count:
                by_status[status_label] = count

        analyses = Analysis.objects.filter(
            document__job_id=job_id, rag_status='done', score__isnull=False
        )
        avg_score = None
        if analyses.exists():
            scores = [a.score for a in analyses if a.score is not None]
            avg_score = round(sum(scores) / len(scores), 1) if scores else None

        lines = [
            f'Vaga: {job.title}',
            f'Status: {job_status_labels.get(job.status, job.status)}',
            f'Criada em: {job.created_at.strftime("%d/%m/%Y")}',
        ]

        if job.description:
            lines.append(f'\nRequisitos / Descrição:\n{job.description}')

        lines.append(f'\nEstatísticas de candidatos (total: {total}):')
        if by_status:
            for label, count in by_status.items():
                lines.append(f'  - {label}: {count}')
        else:
            lines.append('  Nenhum candidato cadastrado ainda.')

        if avg_score is not None:
            lines.append(f'\nScore médio de aderência (RAG): {avg_score}/100')
        else:
            lines.append('\nNenhum candidato com análise RAG concluída.')

        return '\n'.join(lines)
    except Exception as exc:
        logger.error('get_job_summary error: %s', exc)
        return 'Não foi possível obter o resumo da vaga. Tente novamente.'


@tool
def get_top_candidates(job_id: int, user_id: int, limit: int = 5) -> str:
    '''Retorna o ranking dos candidatos com maiores scores de aderência RAG da vaga,
    ordenados do maior para o menor score. Útil para identificar os melhores perfis.

    Args:
        job_id: ID da vaga a ser consultada.
        user_id: ID do usuário autenticado (validação de ownership).
        limit: Número máximo de candidatos a retornar (padrão: 5, máximo: 20).
    '''
    try:
        job = _validate_job_ownership(job_id, user_id)
        if not job:
            return 'Vaga não encontrada ou sem permissão de acesso.'

        Analysis = _get_analysis_model()

        limit = min(max(1, limit), 20)

        top = (
            Analysis.objects
            .filter(document__job_id=job_id, rag_status='done', score__isnull=False)
            .select_related('document')
            .order_by('-score')[:limit]
        )

        if not top:
            return (
                f'Nenhum candidato com análise RAG concluída para a vaga "{job.title}". '
                'Execute a análise de IA nos candidatos primeiro.'
            )

        status_labels = {
            'pending': 'Pendente',
            'reviewing': 'Em análise',
            'approved': 'Aprovado',
            'rejected': 'Reprovado',
        }

        lines = [f'Top {limit} candidatos por score RAG — vaga "{job.title}":\n']
        for i, analysis in enumerate(top, start=1):
            doc = analysis.document
            status_str = status_labels.get(doc.status, doc.status)
            lines.append(
                f'{i}. {doc.candidate_name} | Score: {analysis.score}/100 | Status: {status_str}'
            )

        return '\n'.join(lines)
    except Exception as exc:
        logger.error('get_top_candidates error: %s', exc)
        return 'Não foi possível obter o ranking de candidatos. Tente novamente.'


@tool
def get_candidates_by_status(job_id: int, user_id: int, status: str) -> str:
    '''Retorna a contagem e a lista de candidatos filtrados por um status específico.
    Use esta ferramenta para responder perguntas como "quem está aprovado?" ou
    "quantos candidatos estão em análise?".

    Args:
        job_id: ID da vaga a ser consultada.
        user_id: ID do usuário autenticado (validação de ownership).
        status: Status dos candidatos. Valores válidos: pending (Pendente),
            reviewing (Em análise), approved (Aprovado), rejected (Reprovado).
    '''
    try:
        job = _validate_job_ownership(job_id, user_id)
        if not job:
            return 'Vaga não encontrada ou sem permissão de acesso.'

        valid_statuses = ['pending', 'reviewing', 'approved', 'rejected']
        status_labels = {
            'pending': 'Pendente',
            'reviewing': 'Em análise',
            'approved': 'Aprovado',
            'rejected': 'Reprovado',
        }

        if status not in valid_statuses:
            return (
                f'Status inválido: "{status}". '
                f'Valores válidos: {", ".join(valid_statuses)}.'
            )

        Document = _get_document_model()
        Analysis = _get_analysis_model()

        docs = Document.objects.filter(job_id=job_id, status=status)
        label = status_labels[status]

        if not docs.exists():
            return f'Nenhum candidato com status "{label}" para a vaga "{job.title}".'

        analyses = {
            a.document_id: a
            for a in Analysis.objects.filter(
                document__job_id=job_id, rag_status='done'
            )
        }

        lines = [f'Candidatos com status "{label}" na vaga "{job.title}" ({docs.count()}):\n']
        for doc in docs.order_by('-created_at'):
            lines.append(_format_candidate_row(doc, analyses.get(doc.id)))

        return '\n'.join(lines)
    except Exception as exc:
        logger.error('get_candidates_by_status error: %s', exc)
        return 'Não foi possível filtrar os candidatos. Tente novamente.'


# ---------------------------------------------------------------------------
# Lista de tools registradas no agente
# ---------------------------------------------------------------------------

TOOLS = [
    list_candidates,
    get_candidate_detail,
    get_job_summary,
    get_top_candidates,
    get_candidates_by_status,
]

# ---------------------------------------------------------------------------
# Factory do agente
# ---------------------------------------------------------------------------


def _get_model() -> ChatOpenAI:
    '''Retorna o modelo de linguagem configurado para o agente.'''
    model_name = getattr(settings, 'AGENT_MODEL', 'gpt-4o-mini')
    return ChatOpenAI(model=model_name, temperature=0.3)


def _build_scoped_tools(job_id: int, user_id: int) -> list:
    '''Cria versões das tools com job_id e user_id fixos via closures,
    impedindo que o LLM forneça esses valores livremente.

    Cada tool recebe um wrapper que injeta os valores de contexto da sessão,
    garantindo isolamento entre usuários e vagas.
    '''
    from functools import partial
    from langchain.tools import tool as langchain_tool

    scoped = []

    for base_tool in TOOLS:
        original_func = base_tool.func

        # Determina os parâmetros que não são job_id/user_id
        import inspect
        sig = inspect.signature(original_func)
        extra_params = [
            p for p in sig.parameters
            if p not in ('job_id', 'user_id')
        ]

        if not extra_params:
            # Tool sem parâmetros extras — cria wrapper sem argumentos
            def make_no_param_tool(fn, jid, uid, tname, tdesc):
                @langchain_tool(tname, description=tdesc)
                def scoped_tool() -> str:
                    return fn(job_id=jid, user_id=uid)
                return scoped_tool
            scoped.append(
                make_no_param_tool(
                    original_func, job_id, user_id,
                    base_tool.name, base_tool.description,
                )
            )
        else:
            # Tool com parâmetros extras — usa partial injetando job_id e user_id
            partial_fn = partial(original_func, job_id=job_id, user_id=user_id)
            partial_fn.__doc__ = original_func.__doc__
            partial_fn.__name__ = original_func.__name__

            @langchain_tool(base_tool.name, description=base_tool.description)
            def scoped_tool_with_params(**kwargs) -> str:
                return partial_fn(**kwargs)

            scoped.append(scoped_tool_with_params)

    return scoped


def _serialize_history(history: list[dict]) -> list:
    '''Converte o histórico armazenado no banco (lista de dicts) para
    objetos de mensagem do LangChain.'''
    from langchain_core.messages import HumanMessage, AIMessage

    messages = []
    for entry in history:
        role = entry.get('role', '')
        content = entry.get('content', '')
        if role == 'human':
            messages.append(HumanMessage(content=content))
        elif role == 'ai':
            messages.append(AIMessage(content=content))
    return messages


# ---------------------------------------------------------------------------
# Ponto de entrada público
# ---------------------------------------------------------------------------


def run_hr_agent(
    job_id: int,
    user_id: int,
    user_message: str,
    history: list[dict] | None = None,
) -> dict:
    '''Executa o Agente de RH para uma pergunta do usuário sobre uma vaga.

    O agente usa tools para consultar os dados reais do banco SQLite e
    gera uma resposta em português brasileiro especializada em RH.

    Args:
        job_id: ID da vaga em contexto. Todas as tools são escopadas a esta vaga.
        user_id: ID do usuário autenticado. Usado para validar ownership.
        user_message: Pergunta ou instrução do usuário em linguagem natural.
        history: Lista de mensagens anteriores da conversa. Cada item é um dict
            com as chaves 'role' ('human' ou 'ai') e 'content' (str).
            Passa None ou lista vazia para iniciar nova conversa.

    Returns:
        Dict com:
            - 'response' (str): resposta gerada pelo agente
            - 'history' (list[dict]): histórico atualizado com a nova troca

    Raises:
        Não propaga exceções — retorna dict com chave 'error' em caso de falha.
    '''
    if history is None:
        history = []

    try:
        max_history = getattr(settings, 'AGENT_MAX_HISTORY', 10)

        # Aplica sliding window: mantém apenas as últimas N mensagens
        trimmed_history = history[-(max_history):]

        # Monta o histórico como mensagens LangChain
        prior_messages = _serialize_history(trimmed_history)

        # Cria tools escopadas ao job_id e user_id da sessão
        scoped_tools = _build_scoped_tools(job_id, user_id)

        # Instancia o agente com as tools escopadas
        model = _get_model()
        agent = create_agent(model, tools=scoped_tools, system_prompt=SYSTEM_PROMPT)

        # Monta input: histórico anterior + nova mensagem do usuário
        from langchain_core.messages import HumanMessage
        input_messages = prior_messages + [HumanMessage(content=user_message)]

        # Invoca o agente
        result = agent.invoke({'messages': input_messages})

        # Extrai a resposta da última mensagem AI
        response_message = result['messages'][-1]
        response_content = (
            response_message.content
            if hasattr(response_message, 'content')
            else str(response_message)
        )

        # Atualiza o histórico serializado
        updated_history = trimmed_history + [
            {'role': 'human', 'content': user_message},
            {'role': 'ai', 'content': response_content},
        ]

        return {
            'response': response_content,
            'history': updated_history,
        }

    except Exception as exc:
        logger.error('run_hr_agent error (job_id=%s, user_id=%s): %s', job_id, user_id, exc)
        return {
            'response': (
                'Desculpe, não foi possível processar sua pergunta no momento. '
                'Verifique se a chave da API está configurada e tente novamente.'
            ),
            'history': history,
            'error': str(exc),
        }
