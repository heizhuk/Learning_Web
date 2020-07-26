from django.contrib import admin
from learning_logs.models import Topic,Entry
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id","text")
admin.site.register(Topic,TopicAdmin)
admin.site.register(Entry)
# Register your models here.
