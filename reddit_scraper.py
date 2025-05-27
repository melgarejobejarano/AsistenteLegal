import requests
import json

def get_reddit_post(url):
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request to Reddit's JSON API
        response = requests.get(url + '.json', headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the post content
        post = data[0]['data']['children'][0]['data']
        
        # Print the post title and content
        print("\nTitle:", post['title'])
        print("\nContent:", post['selftext'])
        
        # Save the content to a file
        with open('reddit_post.txt', 'w', encoding='utf-8') as f:
            f.write(f"Title: {post['title']}\n\n")
            f.write(f"Content: {post['selftext']}")
            
        print("\nContent has been saved to 'reddit_post.txt'")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the post: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing the response: {e}")

if __name__ == "__main__":
    url = "https://www.reddit.com/r/learnpython/comments/ng3nq0/what_are_some_must_learn_libraries_in_python/"
    get_reddit_post(url) 