from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Conversation

class ConversationListView(APIView):
    @staticmethod
    def get(request):
        try:
            # 获取所有对话记录
            conversations = Conversation.objects.all()

            # 格式化数据为所需结构
            data = [
                {
                    "role": conversation.status,  # 假设 status 字段表示角色
                    "id": conversation.conversation_id,
                    "title": conversation.title if hasattr(conversation, 'title') else "Untitled",
                    "time": conversation.last_message_time.strftime("%Y-%m-%d %H:%M:%S") if conversation.last_message_time else ""
                }
                for conversation in conversations
            ]

            response = {
                "code": 0,
                "message": "",
                "data": data
            }

        except Exception as e:
            # 处理异常情况
            response = {
                "code": 101,
                "message": str(e),
                "data": []
            }

        return Response(response)