import os
import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# WordPress 클라이언트 설정
wp = Client('https://claysphere1.wordpress.com/xmlrpc.php', os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))

# GPT로 블로그 글 생성
def generate_blog_content():
    try:
        # 본문 생성
        content_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are '봇츠와나', a Countryball character who writes humorous and light-hearted news articles covering politics, climate change, sports, culture, and science."},
                {"role": "user", "content": "Write today's news article in the style described."}
            ]
        )
        content = content_response['choices'][0]['message']['content']

        # 제목 생성
        title_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are '봇츠와나', a Countryball character who writes creative and catchy news headlines."},
                {"role": "user", "content": "Generate a creative title for today's news article."}
            ]
        )
        title = title_response['choices'][0]['message']['content'].strip()

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

if __name__ == "__main__":
    daily_post()
