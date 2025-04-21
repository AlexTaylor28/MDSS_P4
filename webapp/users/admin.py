from django.contrib import admin
from users import models as user_models
from cuoora import models as cuoora_models

admin.site.register(user_models.User)

admin.site.register(cuoora_models.Vote)
admin.site.register(cuoora_models.Question)
admin.site.register(cuoora_models.Answer)
admin.site.register(cuoora_models.Topic)