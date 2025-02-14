from django.contrib import admin
from .models import Conversation, HeritageCard
from rest_framework.authtoken.models import Token



class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'timestamp')  
    search_fields = ('user__username', 'message', 'response')  
    list_filter = ('user', 'timestamp')  

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(HeritageCard)