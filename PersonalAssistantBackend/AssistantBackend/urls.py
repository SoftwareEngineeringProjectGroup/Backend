from django.urls import path
from .views.ConversationListView import ConversationListView

urlpatterns = [
    path('dialogs/lists', ConversationListView.as_view(), name='conversation_list'),
]

