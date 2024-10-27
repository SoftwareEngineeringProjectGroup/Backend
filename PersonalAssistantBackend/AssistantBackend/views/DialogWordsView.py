from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Conversation, ConversationDetail
from datetime import datetime
import time

class DialogWordsView(APIView):
    @staticmethod
    def post(request):
        try:
            # 从请求数据中解析参数
            req_data = request.data
            conversation_id = req_data.get("id")
            role = req_data.get("role")
            model = req_data["data"]["model"]
            message_content = req_data["data"]["messages"]["content"]
            is_code_generation = req_data["data"]["messages"]["is_codegeneration"]
            address = req_data["data"]["messages"]["address"]
            stream = req_data["data"]["stream"]

            # 如果 id 为 0，则创建新的会话记录
            if conversation_id == 0:
                conversation = Conversation.objects.create(status='active')  # 假设 status 表示对话的状态
            else:
                # 查询已存在的会话
                conversation = Conversation.objects.filter(conversation_id=conversation_id).first()
                if not conversation:
                    return Response({"code": 102, "message": "对话ID不存在", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

            # 创建新的消息记录
            conversation_detail = ConversationDetail.objects.create(
                conversation=conversation,
                sender_role="user",
                message_content=message_content
            )

            # 模拟生成的响应数据（在实际情况中，可能需要调用一个外部服务或模型来生成消息）
            response_data = {
                "model": model,
                "created_at": datetime.utcnow().isoformat() + "Z",  # 返回时间戳
                "message": {
                    "role": "assistant",
                    "content": "你好"  # 假设这是生成的内容
                },
                "done": False  # 初始值为 False，后续流式输出
            }

            # 模拟生成过程完成后返回的其他信息
            # 在实际情况中，这些数据应从生成过程获取
            done = True  # 假设处理已完成
            if done:
                response_data.update({
                    "done_reason": "stop",
                    "done": True,
                    "total_duration": 4369972400,    # 假设时间为示例值
                    "load_duration": 3308177200,
                    "prompt_eval_count": 10,
                    "prompt_eval_duration": 48210000,
                    "eval_count": 73,
                    "eval_duration": 1010648000
                })

            # 返回响应
            return Response({"code": 0, "message": "", "data": response_data})

        except Exception as e:
            # 异常处理
            return Response({"code": 102, "message": str(e), "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
