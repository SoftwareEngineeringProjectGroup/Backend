from django.db import models

# Create your models here.

# 4.1 conversations 表
class Conversation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    conversation_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'conversations'


# 4.2 conversation_details 表
class ConversationDetail(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    detail_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'conversation_details'


# 4.3 generation_details 表
class GenerationDetail(models.Model):
    DONE_REASON_CHOICES = [
        ('stop', 'Stop'),
        ('complete', 'Complete'),
    ]

    generation_id = models.AutoField(primary_key=True)
    detail = models.ForeignKey(ConversationDetail, on_delete=models.CASCADE)
    done = models.BooleanField(default=True)
    done_reason = models.CharField(max_length=10, choices=DONE_REASON_CHOICES, default="stop")
    total_duration = models.BigIntegerField(null=True, blank=True)
    load_duration = models.BigIntegerField(null=True, blank=True)
    prompt_eval_count = models.IntegerField(null=True, blank=True)
    prompt_eval_duration = models.BigIntegerField(null=True, blank=True)
    eval_count = models.IntegerField(null=True, blank=True)
    eval_duration = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'generation_details'


# 4.4 document_details 表
class DocumentDetail(models.Model):
    document_id = models.AutoField(primary_key=True)
    detail = models.ForeignKey(ConversationDetail, on_delete=models.CASCADE)

    class Meta:
        db_table = 'document_details'
