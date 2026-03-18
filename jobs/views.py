from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Job, Bid, Contract, Message

# 1. Lista de todos los trabajos abiertos
class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        # Filtramos solo los abiertos y ordenamos por fecha de creación
        return Job.objects.filter(status='OPEN').order_by('-created_at')

# 2. Detalle del trabajo
class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificamos si el usuario ya envió una propuesta
        if self.request.user.is_authenticated:
            context['has_bid'] = Bid.objects.filter(
                job=self.object, 
                freelancer=self.request.user
            ).exists()
        return context

# 3. Crear un nuevo trabajo (Para Clientes)
class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description', 'category', 'budget_type', 'min_budget', 'max_budget']
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

# 4. Enviar una propuesta (Para Freelancers)
class BidCreateView(LoginRequiredMixin, CreateView):
    model = Bid
    fields = ['proposal_text', 'estimated_days', 'bid_amount']
    template_name = 'jobs/bid_form.html'

    def form_valid(self, form):
        form.instance.freelancer = self.request.user
        # Obtenemos el ID del trabajo desde la URL
        form.instance.job = get_object_or_404(Job, id=self.kwargs['job_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.kwargs['job_id']})

# 5. Aceptar una propuesta (Crea el contrato)
class AcceptBidView(LoginRequiredMixin, View):
    def post(self, request, bid_id):
        # Buscamos la propuesta y validamos que el usuario sea el dueño del trabajo
        bid = get_object_or_404(Bid, id=bid_id, job__client=request.user)
        job = bid.job
        
        # Lógica de creación de contrato
        Contract.objects.create(
            job=job,
            bid=bid,
            client=request.user,
            freelancer=bid.freelancer,
            total_amount=bid.bid_amount
        )
        
        # Marcamos el trabajo como "En progreso"
        job.status = 'IN_PROGRESS'
        job.save()
        
        return redirect('job_list')

