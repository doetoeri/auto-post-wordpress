import os
import openai
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# OpenAI API 설정
client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))

# WordPress 클라이언트 설정 (GitHub Secrets에서 사용자 정보 가져옴)
wp = Client('https://claysphere1.wordpress.com/xmlrpc.php', os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))

# GPT로 블로그 글 생성
def generate_blog_content():
    retries = 5
    for attempt in range(retries):
        try:
            # 본문 생성 API 호출
            content_response = client.completions.create(
                model="gpt-3.5-turbo",  # 최신 GPT 모델 사용
                prompt="Write a detailed blog post about technology trends in 2024",
                max_tokens=1000
            )
            content = content_response['choices'][0]['text']

            # 제목 생성 API 호출
            title_response = client.completions.create(
                model="gpt-3.5-turbo",  # 최신 GPT 모델 사용
                prompt="Generate a creative title for a blog post about technology trends in 2024",
                max_tokens=10
            )
            title = title_response['choices'][0]['text'].strip()

            return title, content
        
        except openai.error.RateLimitError:
            logging.error(f"Rate limit exceeded. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # 지수 백오프 전략 적용
        except Exception as e:
            logging.error(f"Error generating blog content: {e}")
            return None, None
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

if __name__ == "__main__":
    daily_post()
