import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import BookRating
import os
from dotenv import load_dotenv

import redis
import json
import numpy as np
import ssl

# Load environment variables
load_dotenv()

# Redis configuration with SSL handling
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
try:
    # For Heroku Redis with SSL
    if REDIS_URL.startswith('rediss://'):
        # Create a custom connection class that skips certificate validation
        class SSLConnection(redis.Connection):
            def __init__(self, **kwargs):
                kwargs['ssl_cert_reqs'] = ssl.CERT_NONE
                super().__init__(**kwargs)
        
        # Create a connection pool with our custom class
        pool = redis.ConnectionPool.from_url(
            REDIS_URL,
            connection_class=SSLConnection
        )
        redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
    else:
        # For local Redis without SSL
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    
    # Test the connection
    redis_client.ping()
    print("Redis connection successful")
except Exception as e:
    print(f"Redis connection error: {e}")
    # Fallback to a dummy client that doesn't throw errors
    class DummyRedisClient:
        def get(self, key):
            return None
        def setex(self, key, time, value):
            pass
    redis_client = DummyRedisClient()
    print("Using dummy Redis client")

# Replacing spaCy + transformers
# We'll use TF-IDF for keyword extraction and similarity

# ----------------------
# 1. Keyword Extraction
# ----------------------
def extract_keywords(text, n=7):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=n)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_arr = vectorizer.get_feature_names_out()
    tfIdf_sorting = tfidf_matrix.toarray().flatten().argsort()[::-1]

    return [feature_arr[i] for i in tfIdf_sorting[:n]]


# --------------------------
# 2. Google Books Fetch
# --------------------------
def fetch_books_from_google_api(query):
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    recommendations = []

    start_index = 0
    max_results = 40
    filtered_categories = [
        "fiction", "drama", "adventure", "fantasy", "horror", "action", "comedy", "history", "western",
        "crime", "mystery", "romance", "magic", "family", "war", "kids", "children", "sci-fi", "comic", "novel", "graphic"
    ]

    try:
        while len(recommendations) < max_results:
            url = "https://www.googleapis.com/books/v1/volumes"
            query_string = f"{query['keywords']} {query['genre']}"
            query_string_title = f"{query['title']}"

            param_list = {
                "q": query_string,
                "maxResults": 40,
                "startIndex": start_index,
                "key": api_key
            }

            param_list_title = {
                "q": query_string_title,
                "maxResults": 5,
                "startIndex": start_index,
                "key": api_key
            }

            response_title = requests.get(url, params=param_list_title)
            response_title.raise_for_status()
            books_title_data = response_title.json()

            for book in books_title_data.get("items", []):
                volumeInfo = book.get("volumeInfo", {})
                categories = volumeInfo.get("categories", [])

                if not categories or not any(any(fc in category.lower() for fc in filtered_categories) for category in categories):
                    continue

                recommendations.append({
                    "id": book.get("id"),
                    "title": volumeInfo.get("title", "Unknown Title"),
                    "authors": volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date": volumeInfo.get("publishedDate", "Unknown"),
                    "description": volumeInfo.get("description", "No Description Available"),
                    "categories": categories,
                    "image": volumeInfo.get("imageLinks", {}).get("thumbnail")
                })

            response = requests.get(url, params=param_list)
            response.raise_for_status()
            books_data = response.json()

            for book in books_data.get("items", []):
                volumeInfo = book.get("volumeInfo", {})
                categories = volumeInfo.get("categories", [])

                if not categories or not any(any(fc in category.lower() for fc in filtered_categories) for category in categories):
                    continue

                recommendations.append({
                    "id": book.get("id"),
                    "title": volumeInfo.get("title", "Unknown Title"),
                    "authors": volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date": volumeInfo.get("publishedDate", "Unknown"),
                    "description": volumeInfo.get("description", "No Description Available"),
                    "categories": categories,
                    "image": volumeInfo.get("imageLinks", {}).get("thumbnail")
                })

            start_index += len(books_data.get("items", []))
            if len(books_data.get("items", [])) < 40:
                break

        dupe_title_date = set()
        final_recommendations = []

        for book in recommendations:
            if (book["title"], book["published_date"]) not in dupe_title_date:
                final_recommendations.append(book)
                dupe_title_date.add((book["title"], book["published_date"]))

        return final_recommendations

    except Exception as e:
        print(f"Error fetching books: {e}")
        return []


def fetch_books_from_google_api_using_id(id):
    url = f"https://www.googleapis.com/books/v1/volumes/{id}"
    response = requests.get(url)
    response.raise_for_status()
    book_data = response.json()

    volumeInfo = book_data.get("volumeInfo", {})
    categories = volumeInfo.get("categories", [])
    description = volumeInfo.get("description", "No Description Available")

    for tag in ["<p>", "</p>", "<br>", "</br>", "<b>", "</b>", "<i>", "</i>"]:
        description = description.replace(tag, "")

    return {
        "id": book_data.get("id"),
        "title": volumeInfo.get("title", "Unknown Title"),
        "authors": volumeInfo.get("authors", ["Unknown Author"]),
        "published_date": volumeInfo.get("publishedDate", "Unknown"),
        "description": description,
        "categories": categories[:3],
        "image": volumeInfo.get("imageLinks", {}).get("thumbnail")
    }


# ----------------------------------------------
# 3. Lightweight Collaborative Filtering (pandas)
# ----------------------------------------------
def get_collaborative_filtering_recommendations():
    user_ratings = BookRating.objects.all()

    if not user_ratings:
        return []

    df = pd.DataFrame(list(user_ratings.values("user__id", "book_id", "rating")))
    pivot = df.pivot_table(index='user__id', columns='book_id', values='rating').fillna(0)

    cosine_sim = cosine_similarity(pivot.T)
    sim_df = pd.DataFrame(cosine_sim, index=pivot.columns, columns=pivot.columns)

    mean_scores = sim_df.mean(axis=1).sort_values(ascending=False)

    top_books = mean_scores.head(10).index.tolist()

    return [fetch_books_from_google_api_using_id(book_id) for book_id in top_books]


# -------------------------------------
# 4. Rank by TF-IDF Cosine Similarity
# -------------------------------------
def rank_books_by_cosine_similarity(media_query, books):
    book_descriptions = [book.get("description", "") for book in books]
    book_titles = [book.get("title", "") for book in books]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(book_descriptions + [media_query["description"]])

    similarity_scores = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
    ranked = sorted(zip(books, similarity_scores), key=lambda x: x[1], reverse=True)

    return [book for book, score in ranked][:39]


# -------------------------------
# 5. Final Recommendation Flow
# -------------------------------
def get_recommended_books(media_query):
    print(f"Getting recommendations for: {media_query.get('title', '')}")
    
    # Create a simplified cache key that's more likely to match for similar queries
    # Only use title and genre for the cache key
    simplified_query = {
        'title': media_query.get('title', '').lower().strip(),
        'genre': media_query.get('genre', '').lower().strip()
    }
    
    cache_key = f"recommendations:{json.dumps(simplified_query, sort_keys=True)}"
    print(f"Cache key: {cache_key}")
    
    try:
        # Try to get cached recommendations
        cached_recommendations = redis_client.get(cache_key)
        if cached_recommendations:
            print("✅ CACHE HIT! Fetching recommendations from cache")
            return json.loads(cached_recommendations)
        else:
            print("❌ CACHE MISS! No cached recommendations found")
    except Exception as e:
        print(f"Redis error when reading cache (non-critical): {e}")
        # Continue without caching

    print("Generating new recommendations...")
    media_query["keywords"] = extract_keywords(media_query.get("description", ""))

    books = fetch_books_from_google_api(media_query)
    try:
        collab_books = get_collaborative_filtering_recommendations()
        print(f"Got {len(collab_books)} collaborative filtering recommendations")
        books += collab_books
    except Exception as e:
        print(f"Error getting collaborative recommendations: {e}")
    
    print(f"Found {len(books)} total books before ranking")
    ranked_book_recommendations = rank_books_by_cosine_similarity(media_query, books)
    print(f"Returning {len(ranked_book_recommendations)} ranked recommendations")

    # Cache the results for 30 minutes (1800 seconds)
    try:
        json_data = json.dumps(ranked_book_recommendations)
        redis_client.setex(cache_key, 1800, json_data)
        print(f"✅ Successfully cached recommendations with key: {cache_key}")
    except Exception as e:
        print(f"Redis caching error (non-critical): {e}")

    return ranked_book_recommendations
