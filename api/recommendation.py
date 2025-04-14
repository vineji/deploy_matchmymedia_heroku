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

# Load environment variables
load_dotenv()

# Redis remains unchanged
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Replacing spaCy + transformers
# We'll use TF-IDF for keyword extraction and similarity

# ----------------------
# 1. Keyword Extraction
# ----------------------
def extract_keywords(text, n=7):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=n)
    tfidf_matrix = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()


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
    cache_key = f"final_recommendations:{json.dumps(media_query, sort_keys=True)}"

    try:
        cached_recommendations = redis_client.get(cache_key)
        if cached_recommendations:
            print("Fetching final recommendations from cache")
            return json.loads(cached_recommendations)
    except ConnectionError:
        print("Redis connect error. Provide recommendations without caching")

    media_query["keywords"] = extract_keywords(media_query["description"])

    books = fetch_books_from_google_api(media_query)
    books += get_collaborative_filtering_recommendations()

    ranked_book_recommendations = rank_books_by_cosine_similarity(media_query, books)

    try:
        redis_client.setex(cache_key, 1200, json.dumps(ranked_book_recommendations))
    except ConnectionError:
        print("Redis connect error. Skip cache writing")

    return ranked_book_recommendations
