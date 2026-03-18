from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = (
        ('CLIENT', 'Cliente'),
        ('FREELANCER', 'Freelancer'),
        ('BOTH', 'Ambos'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='FREELANCER')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.FloatField(default=0.0)
    
    # Campos de Redes/Contacto (Estilo Cyberpunk)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class PortfolioItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/')
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

# Signals para crear el perfil automáticamente al crear un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Job(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Abierto'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    )
    
    PAYMENT_TYPE = (
        ('FIXED', 'Presupuesto Fijo'),
        ('HOURLY', 'Pago por Hora'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    required_skills = models.ManyToManyField(Skill, blank=True)
    
    budget_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default='FIXED')
    min_budget = models.DecimalField(max_digits=10, decimal_places=2)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.client.username}"

class Bid(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bids')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_bids')
    proposal_text = models.TextField()
    estimated_days = models.IntegerField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evitamos que un freelancer puje dos veces por el mismo trabajo
        unique_together = ('job', 'freelancer')

    def __str__(self):
        return f"{self.freelancer.username} -> {self.job.title} (${self.bid_amount})"


class Contract(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'En Curso'),
        ('COMPLETED', 'Finalizado'),
        ('DISPUTE', 'En Disputa'),
        ('CANCELLED', 'Cancelado'),
    )

    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='contract')
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name='contract_origin')
    
    # Referencias directas para facilitar consultas
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_client')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts_as_freelancer')
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Contrato: {self.job.title} ({self.freelancer.username})"

class Milestone(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('IN_REVIEW', 'En Revisión'),
        ('PAID', 'Pagado'),
    )

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.contract.job.title} (${self.amount})"


class Message(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    file_attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"De {self.sender.username} en {self.contract.job.title}"

