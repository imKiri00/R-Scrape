import argparse
import psycopg2
from .config import load_config
from .providers import get_provider

def evaluate_post(post_content, provider):
    """
    Evaluate a single post using the specified AI provider.
    
    Args:
        post_content (str): The content of the post to be evaluated.
        provider (object): An instance of the AI provider class.
    
    Returns:
        float: The evaluation score for the post.
    """
    return provider.evaluate(post_content)

def evaluate_all_unrated_posts(provider_name="llama"):
    """
    Evaluate all unrated posts in the database using the specified provider.
    
    Args:
        provider_name (str): The name of the AI provider to use.
    
    Returns:
        int: The number of posts evaluated.
    """
    config = load_config()
    provider = get_provider(provider_name, config)

    db_config = config['database']
    conn = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        dbname=db_config['name'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM reddit_posts WHERE evaluation_score IS NULL")
    posts = cursor.fetchall()

    for post_id, post_content in posts:
        evaluation_score = evaluate_post(post_content, provider)
        cursor.execute(
            "UPDATE reddit_posts SET evaluation_score = %s WHERE id = %s",
            (evaluation_score, post_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return len(posts)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Evaluate Reddit posts using AI")
    parser.add_argument("--provider", default="llama", choices=["llama", "ollama", "groq"], help="AI provider to use")
    args = parser.parse_args()

    num_evaluated = evaluate_all_unrated_posts(args.provider)
    print(f"Evaluated {num_evaluated} posts using {args.provider} provider.")

if __name__ == "__main__":
    main()