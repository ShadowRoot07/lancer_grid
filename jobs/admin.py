from django.contrib import admin
from .models import Profile, Skill, PortfolioItem, Job, Bid, Contract, Milestone

admin.site.register(Contract)
admin.site.register(Milestone)
admin.site.register(Job)
admin.site.register(Bid)
admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(PortfolioItem)

