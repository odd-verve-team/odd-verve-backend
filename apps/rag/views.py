import os

from django.http import JsonResponse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rest_framework.decorators import api_view

from apps.rag.models import ChatMessage, ChatSession, ChatRolesTextChoices
from apps.rag.search import search

load_dotenv()


@api_view(["POST"])
def ai(request) -> JsonResponse:

    message = request.data.get("message", "").strip()
    chat_id = request.data.get("chat_id")
    user_id = request.user.id if request.user.is_authenticated else None

    if not user_id:
        return JsonResponse({"Error": "user is not authenticated"}, status=401)

    if not message:
        return JsonResponse({"Error": "message can not be empty"}, status=400)
    try:
        documents = search(query=message)
        context = "\n\n".join([f"[{d['title']}]\n{d['body']}" for d in documents])
        prompt = f"""Answer the question based on the documents below.
    
        # Documents
        {context}
    
        # User message
        {message}
    
        # Answer (concise, grounded in the documents above)"""

        if chat_id:
            try:
                chat = ChatSession.objects.get(id=chat_id, user_id=user_id)
            except ChatSession.DoesNotExist:
                return JsonResponse({"Error": "chat is not found"}, status=404)
        else:
            chat = ChatSession.objects.create(user_id=user_id)

        history = []
        messages = ChatMessage.objects.filter(session_id=chat.id).order_by("created_at")
        for message_object in messages.values("role", "message"):
            history.append({"role": message_object["role"], "parts": [{"text": message_object["message"]}]})
        history = history if history else None
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model = client.chats.create(
            model="gemini-2.5-flash",
            history=history,
            config=types.GenerateContentConfig(
                system_instruction="You are ai helper in the online gallery site. "
                                   "Your task is helping users to understand how does "
                                   "this site work. If there is no related information "
                                   "in documents then you tell user that you do not know the answer"
            )
        )
        response = model.send_message(prompt)
        ChatMessage.objects.create(session=chat, role=ChatRolesTextChoices.USER, message=message)
        ChatMessage.objects.create(session=chat, role=ChatRolesTextChoices.MODEL, message=response.text)
        return JsonResponse({"model": response.text, "chat_id": chat.id}, status=200)
    except Exception as error:
        return JsonResponse({"Error": str(error)}, status=500)
