from gigachat import GigaChat
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_ai_comment(data, risk_score):
    prompt = f"""
    Клиент:
    возраст: {data.get("age")}
    доход: {data.get("income")}
    работа: {data.get("job")}
    риск: {risk_score}

    Дай краткое объяснение решения банка.
    """

    response_text = ""

    try:
        with GigaChat(
            credentials=getenv("GIGA_TOKEN"),
            verify_ssl_certs=False
        ) as client:

            for chunk in client.stream(prompt):
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
    except Exception as e:
        response_text = f"Не удалось получить комментарий ИИ: {str(e)}"

    return response_text