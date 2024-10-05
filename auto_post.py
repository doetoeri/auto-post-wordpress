import os
import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import schedule
import time

# OpenAI API 키를 GitHub Secrets에서 가져옴
openai.api_key = os.getenv('OPENAI_API_KEY')

# WordPress 클라이언트 설정 (GitHub Secrets에서 사용자 정보 가져옴)
wp = Client('https://claysphere1.wordpress.com/xmlrpc.php', os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))

# GPT로 블로그 글 생성
def generate_blog_content():
    # 글 본문 생성
    content_response = openai.Completion.create(
        engine="text-davinci-003",  # 사용할 GPT 모델
        prompt="'삐릿...dumelang! 봇츠와나 입니다!'로 시작하는 재미있는 컨트리볼 이야기를 만들어주세요. 이야기는 'made by BOTswana&counballchan'으로 끝나게 해주세요. 한국어로 작성해주세요.",  # 원하는 주제
        max_tokens=1000
    )
    content = content_response['choices'][0]['text']
    
    # 글 제목 생성
    title_response = openai.Completion.create(
        engine="text-davinci-003",  # 사용할 GPT 모델
        prompt="Generate a creative title for a blog post about technology trends in 2024",
        max_tokens=10
    )
    title = title_response['choices'][0]['text'].strip()  # 제목에서 불필요한 공백 제거

    return title, content

# 워드프레스에 글 업로드
def post_to_wordpress(title, content):
    post = WordPressPost()
    post.title = title  # 자동 생성된 제목
    post.content = content
    post.post_status = 'publish'
    wp.call(NewPost(post))

# 블로그 글 작성 및 업로드
def daily_post():
    title, content = generate_blog_content()
    post_to_wordpress(title, content)

# 매일 6시에 실행되도록 설정
schedule.every().day.at("06:00").do(daily_post)

# 계속 실행 상태 유지
while True:
    schedule.run_pending()
    time.sleep(60)
