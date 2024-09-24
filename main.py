from openai import OpenAI
from openai.types.chat import ChatCompletion

import config
from consumer import start_consume

__OPENAI_API_KEY: str = config.get_key()

def create_shorts_title_gpt(subscription):
    client = OpenAI(
        api_key=__OPENAI_API_KEY
    )

    model = "gpt-4o-mini"
    query = ("Convert the following subscription into a Youtube Shorts title. "
             "The Shorts title should be in the same language as the original title and should be under 20 characters long. "
             f"Do not include special symbols or emojis. YouTube title : {subscription}")

    messages = [{
        "role": "system",
        "content": ("You are an expert in generating catchy and engaging titles specifically for YouTube Shorts. "
                   "Your goal is to create titles that are eye-catching and entertaining.")
    }, {
        "role": "user",
        "content": query
    }]

    try:
        response: ChatCompletion = client.chat.completions.create(model=model,
                                                      messages=messages,
                                                      timeout=10.0)
    except Exception as e:
        raise RuntimeError(e, "chat gpt api에서 오류가 발생했습니다")
    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("chat gpt로부터 답을 받지 못했습니다")

    return answer

def test_start():
    subscription = ""
    with open('test_subscription.txt', 'r') as file:
        for line in file.readlines():
            subscription += line

    answer = create_shorts_title_gpt(subscription)
    print(answer)

def start():
    start_consume()

if __name__ == "__main__":
    start()