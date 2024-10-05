import openai
import requests

def generate_blog_content():
    try:
        # 본문 생성 API 호출 (30초 타임아웃)
        content_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Write a detailed blog post about technology trends in 2024",
            max_tokens=1000,
            timeout=30  # 30초 타임아웃
        )
        content = content_response['choices'][0]['text']
        
        # 제목 생성 API 호출 (10초 타임아웃)
        title_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Generate a creative title for a blog post about technology trends in 2024",
            max_tokens=10,
            timeout=10  # 10초 타임아웃
        )
        title = title_response['choices'][0]['text'].strip()

        return title, content
    
    except requests.exceptions.Timeout:
        print("OpenAI API 응답 시간이 초과되었습니다.")
        return None, None
