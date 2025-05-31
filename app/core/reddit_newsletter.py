import praw
import time
import os
import requests
import json
from datetime import datetime

# OpenRouter configuration
model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter key stored as OPENAI_API_KEY
base_url = "https://openrouter.ai/api/v1"  # OpenRouter endpoint

def make_openrouter_request(messages, max_tokens=1500, temperature=0.7):
    """Make a direct HTTP request to OpenRouter API"""
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required (contains OpenRouter key)")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",  # OpenRouter requirement
        "X-Title": "Reddit Newsletter Generator"  # OpenRouter requirement
    }
    
    data = {
        "model": model_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenRouter API request failed: {e}")
        raise

def scrape_reddit(subreddit_name="LocalLLaMA", max_comments_per_post=7):
    """Scrape Reddit content from specified subreddit"""
    # Get Reddit credentials from environment variables
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "demo-client-id")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "demo-client-secret")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "demo-user-agent")
    
    try:
        reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent,
        )
        subreddit = reddit.subreddit(subreddit_name)
        scraped_data = []

        for post in subreddit.hot(limit=12):
            post_data = {"title": post.title, "url": post.url, "comments": []}

            try:
                post.comments.replace_more(limit=0)  # Load top-level comments only
                comments = post.comments.list()
                if max_comments_per_post is not None:
                    comments = comments[:max_comments_per_post]

                for comment in comments:
                    post_data["comments"].append(comment.body)

                scraped_data.append(post_data)

            except praw.exceptions.APIException as e:
                print(f"API Exception: {e}")
                time.sleep(60)  # Sleep for 1 minute before retrying

        return scraped_data
    except Exception as e:
        print(f"Reddit scraping failed for r/{subreddit_name}: {e}")
        # Return demo data if Reddit fails
        return get_demo_data(subreddit_name)

def get_demo_data(subreddit_name="LocalLLaMA"):
    """Return demo data when Reddit API is not available"""
    if subreddit_name.lower() in ["localllama", "local_llama"]:
        return [
            {
                "title": "New Open Source LLM Model Released",
                "url": "https://github.com/example/new-llm",
                "comments": [
                    "This looks amazing! Finally a good open source alternative.",
                    "The performance benchmarks are impressive.",
                    "Can't wait to try this on my local setup."
                ]
            },
            {
                "title": "Local LLaMA Performance Optimization Tips",
                "url": "https://reddit.com/r/LocalLLaMA/example",
                "comments": [
                    "These optimization tips increased my inference speed by 40%!",
                    "The quantization method mentioned here is game-changing.",
                    "Thanks for sharing, this helped me a lot."
                ]
            },
            {
                "title": "Running 70B Models on Consumer Hardware",
                "url": "https://huggingface.co/example",
                "comments": [
                    "I managed to run this on my RTX 4090 with 24GB VRAM.",
                    "The memory optimization techniques are brilliant.",
                    "This opens up so many possibilities for home users."
                ]
            }
        ]
    else:
        # Generic demo data for other subreddits
        return [
            {
                "title": f"Popular Discussion in r/{subreddit_name}",
                "url": f"https://reddit.com/r/{subreddit_name}/example1",
                "comments": [
                    "This is really interesting!",
                    "Thanks for sharing this with the community.",
                    "I learned something new today."
                ]
            },
            {
                "title": f"Trending Topic in r/{subreddit_name}",
                "url": f"https://reddit.com/r/{subreddit_name}/example2",
                "comments": [
                    "Great find! This deserves more attention.",
                    "The community really benefits from posts like this.",
                    "Looking forward to more content like this."
                ]
            },
            {
                "title": f"Community Insights from r/{subreddit_name}",
                "url": f"https://reddit.com/r/{subreddit_name}/example3",
                "comments": [
                    "This aligns with my experience as well.",
                    "Thanks for the detailed explanation.",
                    "The community is so helpful and knowledgeable."
                ]
            }
        ]

def analyze_content(scraped_data, subreddit_name="LocalLLaMA"):
    """Analyze scraped Reddit content using AI"""
    content_summary = ""
    for post in scraped_data:
        content_summary += f"Title: {post['title']}\nURL: {post['url']}\n"
        content_summary += f"Comments: {' | '.join(post['comments'][:3])}\n\n"
    
    prompt = f"""
    Analyze the following Reddit posts from r/{subreddit_name} and create a detailed report on the key trends, discussions, and insights:

    {content_summary}

    Please provide:
    1. A summary of the most important topics being discussed
    2. Key trends and themes in the r/{subreddit_name} community
    3. Notable insights, tools, or resources mentioned
    4. Your analysis of how these discussions reflect the community's interests and concerns

    Focus on what matters most to the r/{subreddit_name} community and provide valuable insights.
    """

    try:
        return make_openrouter_request([{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.7)
    except Exception as e:
        print(f"AI analysis failed: {e}")
        return f"AI analysis temporarily unavailable. Please check your OpenRouter configuration."

def create_newsletter(analysis, scraped_data, subreddit_name="LocalLLaMA"):
    """Create a formatted newsletter from the analysis"""
    newsletter_prompt = f"""
    Based on this analysis of r/{subreddit_name} content, create an engaging newsletter in markdown format:

    {analysis}

    Original posts for reference:
    {chr(10).join([f"- [{post['title']}]({post['url']})" for post in scraped_data[:5]])}

    Create a newsletter with:
    1. An engaging headline that mentions r/{subreddit_name}
    2. 3-5 main sections highlighting different topics/trends
    3. Use this exact markdown format for each section:

    ## [Topic/Discussion Title](URL)
    - Key facts and interesting details
    - Why this matters to the r/{subreddit_name} community
    - Your thoughts on implications for the community

    Make it engaging, informative, and tailored to the r/{subreddit_name} community interests.
    Include the actual URLs from the Reddit posts where relevant.
    """

    try:
        return make_openrouter_request([{"role": "user", "content": newsletter_prompt}], max_tokens=2000, temperature=0.8)
    except Exception as e:
        print(f"Newsletter creation failed: {e}")
        return f"# r/{subreddit_name} Newsletter - {datetime.now().strftime('%B %d, %Y')}\n\nNewsletter generation temporarily unavailable. Please check your OpenRouter configuration.\n\n## Recent Posts\n" + "\n".join([f"- [{post['title']}]({post['url']})" for post in scraped_data[:5]])

class SimpleNewsletter:
    """Simple newsletter generator without CrewAI"""
    
    def kickoff(self, subreddit_name="LocalLLaMA"):
        """Generate the newsletter for specified subreddit"""
        print(f"🔍 Scraping Reddit content from r/{subreddit_name}...")
        scraped_data = scrape_reddit(subreddit_name)
        
        print("🤖 Analyzing content with AI...")
        analysis = analyze_content(scraped_data, subreddit_name)
        
        print("📰 Creating newsletter...")
        newsletter = create_newsletter(analysis, scraped_data, subreddit_name)
        
        return newsletter

# Create a simple crew-like interface
crew = SimpleNewsletter()

# Only run this if the script is executed directly (not imported)
if __name__ == "__main__":
    # Get your newsletter!
    result = crew.kickoff()

    print("######################")
    print(result)
