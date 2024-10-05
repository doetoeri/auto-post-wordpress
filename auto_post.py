import os
import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import logging
import schedule
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# OpenAI API 키를 GitHub Secrets에서 가져옴
openai.api_key = os.getenv('OPENAI_API_KEY')

# WordPress 클라이언트 설정 (GitHub Secrets에서 사용자 정보 가져옴)
wp = Client('https://claysphere1.wordpress.com/xmlrpc.php', os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))

# GPT로 블로그 글 생성
def generate_blog_content():
    try:
        content_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Write a detailed blog post about technology trends in 2024",
            max_tokens=1000
        )
        content = content_response['choices'][0]['text'].strip()
        
        title_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Generate a creative title for a blog post about technology trends in 2024",
            max_tokens=10
        )
        title = title_response['choices'][0]['text'].strip()

        return title, content
    
    except Exception as e:
        logging.error(f"Error generating blog content: {e}")
        return None, None

# 워드프레스에 글 업로드
def post_to_wordpress(title, content):
    try:
        post = WordPressPost()
        post.title = title  # 자동 생성된 제목
        post.content = content
        post.post_status = 'publish'
        post_id = wp.call(NewPost(post))  # 게시물 ID 반환
        logging.info(f"Post uploaded successfully. Post ID: {post_id}")
    except Exception as e:
        logging.error(f"Error uploading post to WordPress: {e}")

# 블로그 글 작성 및 업로드
def daily_post():
    title, content = generate_blog_content()
    if title and content:
        post_to_wordpress(title, content)
    else:
        logging.error("No title or content generated.")

# 매일 6시에 실행되도록 설정
schedule.every().day.at("06:00").do(daily_post)

# 계속 실행 상태 유지
while True:
    schedule.run_pending()
    time.sleep(60)
