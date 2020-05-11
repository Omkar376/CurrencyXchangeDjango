from django.contrib import admin

# Register your models here.
# the module name is app_name.models
from users.models import User

admin.site.register(User)