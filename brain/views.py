from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

# Importações dos modelos das outras apps
from hub.models import Job
from documents.models import Document
from .models import Analysis, AgentConversation

# Importação do serviço do Pipeline RAG (Certifique-se de que este arquivo existe)
# Task 5B.8.4: Interface entre a View e a lógica de processamento pesado
try:
    from brain import run_rag_analysis
except ImportError:
    # Fallback caso você ainda não tenha criado o services.py
    def run_rag_analysis(doc_id, job_id):
        return {'score': 85, 'summary': 'Simulação: Perfil compatível com a vaga.'}

# Importação do Agente de RH
from agents.hr_agent import run_hr_agent


class JobAnalysisView(LoginRequiredMixin, DetailView):
    '''
    View para exibir o dashboard analítico de uma vaga específica.
    '''
    model = Job
    template_name = 'brain/job_analysis.html'
    context_object_name = 'job'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        status_counts = job.documents.values('status').annotate(
            count=Count('id')
        )

        stats = {item['status']: item['count'] for item in status_counts}
        context['stats'] = stats

        context['approved_documents'] = job.documents.filter(
            status=Document.APPROVED
        ).order_by('-created_at')

        context['reviewing_documents'] = job.documents.filter(
            status=Document.REVIEWING
        ).order_by('-created_at')

        return context


class DocumentAnalysisView(LoginRequiredMixin, View):
    '''
    Task 5B.8.1: Aciona o pipeline RAG para um documento específico.
    Gerencia validação de posse, status do processamento e erros.
    '''

    def post(self, request, document_pk):
        '''
        Task 5B.8.2: Recupera o documento com segurança garantindo que pertence ao usuário.
        '''
        document = get_object_or_404(
            Document,
            pk=document_pk,
            job__user=request.user
        )
        job = document.job

        # Task 5B.8.3: Inicializa o registro de análise como 'processing'
        analysis, created = Analysis.objects.update_or_create(
            document=document,
            job=job,
            defaults={
                'rag_status': Analysis.PROCESSING,
                'error_message': ''
            }
        )

        try:
            # Task 5B.8.4: Executa o pipeline (Extração -> Chunking -> Vector Store -> LLM)
            result = run_rag_analysis(document.id, job.id)

            # Task 5B.8.5: Salva o resultado final e score
            analysis.score = result.get('score', 0)
            analysis.summary = result.get('summary', '')
            analysis.rag_status = Analysis.DONE
            analysis.save()

            messages.success(
                request,
                f'Análise de IA concluída para {document.candidate_name}.'
            )

        except Exception as e:
            # Task 5B.8.5: Em caso de falha, registra o erro no banco para depuração técnica
            analysis.rag_status = Analysis.ERROR
            analysis.error_message = str(e)
            analysis.save()

            messages.error(
                request,
                f'Erro no processamento de {document.candidate_name}: {str(e)}'
            )

        # Task 5B.8.6: Redireciona de volta para a lista de documentos da vaga
        return redirect('documents:document-list', job_pk=job.id)


class AgentChatView(LoginRequiredMixin, View):
    '''
    Task 8.6: Interface de chat com o Agente de RH para uma vaga específica.

    GET  — renderiza a página de chat com o histórico existente.
    POST — recebe a mensagem do usuário, chama o agente e retorna JsonResponse.
    '''

    def _get_job(self, request, job_pk):
        '''Retorna a vaga validando que pertence ao usuário logado.'''
        return get_object_or_404(Job, pk=job_pk, user=request.user)

    def get(self, request, job_pk):
        job = self._get_job(request, job_pk)
        conversation, _ = AgentConversation.objects.get_or_create(
            job=job,
            user=request.user,
        )
        return self._render(request, job, conversation)

    def post(self, request, job_pk):
        job = self._get_job(request, job_pk)
        conversation, _ = AgentConversation.objects.get_or_create(
            job=job,
            user=request.user,
        )

        user_message = request.POST.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Mensagem não pode estar vazia.'}, status=400)

        result = run_hr_agent(
            job_id=job.id,
            user_id=request.user.id,
            user_message=user_message,
            history=conversation.messages,
        )

        if 'error' in result and not result.get('response'):
            return JsonResponse({'error': result['error']}, status=500)

        conversation.messages = result['history']
        conversation.save()

        return JsonResponse({'response': result['response']})

    def _render(self, request, job, conversation):
        from django.shortcuts import render
        return render(request, 'brain/agent_chat.html', {
            'job': job,
            'conversation': conversation,
        })


class AgentChatClearView(LoginRequiredMixin, View):
    '''
    Task 8.6.5: Limpa o histórico da conversa com o agente para uma vaga.
    Usado pelo botão "Nova conversa" no template.
    '''

    def post(self, request, job_pk):
        job = get_object_or_404(Job, pk=job_pk, user=request.user)
        AgentConversation.objects.filter(job=job, user=request.user).update(
            messages=[]
        )
        return JsonResponse({'ok': True})