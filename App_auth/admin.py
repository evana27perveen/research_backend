from django.contrib import admin
from App_auth.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AdminProfileModel)
admin.site.register(ResearcherProfileModel)
admin.site.register(ReaderProfileModel)
admin.site.register(ReviewerProfileModel)
