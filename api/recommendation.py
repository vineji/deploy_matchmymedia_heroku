import requests
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from .models import BookRating
import os
from dotenv import load_dotenv
import json
import hashlib
from numpy import dot
from numpy.linalg import norm
import numpy as np

from django.core.cache import cache

# Load environment variables
load_dotenv()

# NLP
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model not found, download it and load it
    print("spaCy model not found. Downloading en_core_web_sm...")
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Hugging Face API setup
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}


def get_embeddings_batch(texts, batch_size=20):
    """Get sentence embeddings in batches from Hugging Face API"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = requests.post(HUGGINGFACE_API_URL, headers=headers, json={"inputs": batch})
            response.raise_for_status()
            
            batch_embeddings = response.json()
            all_embeddings.extend(batch_embeddings)
            
            print(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        except requests.RequestException as e:
            print(f"Embedding API error in batch {i//batch_size + 1}: {e}")
            # Add empty embeddings as fallback
            all_embeddings.extend([[] for _ in range(len(batch))])
    
    return all_embeddings


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors"""
    if not vec1 or not vec2:
        return 0.0
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# --------------------------
# Google Books Fetch
# --------------------------
def fetch_books_from_google_api(query):
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    recommendations = []
    start_index = 0
    max_results = 40

    filtered_categories = [
        "fiction", "drama", "adventure", "fantasy", "horror", "action", "comedy", "western",
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
                "maxResults": 3,
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

    phrases_to_remove = ["<p>", "</p>", "<br>", "</br>", "<b>", "</b>", "<i>", "</i>"]
    description = volumeInfo.get("description", "No Description Available")

    for x in phrases_to_remove:
        description = description.replace(x, "")

    return {
        "id": book_data.get("id"),
        "title": volumeInfo.get("title", "Unknown Title"),
        "authors": volumeInfo.get("authors", ["Unknown Author"]),
        "published_date": volumeInfo.get("publishedDate", "Unknown"),
        "description": description,
        "categories": categories[:3],
        "image": volumeInfo.get("imageLinks", {}).get("thumbnail")
    }


def extract_keywords(text, n=7):
    if nlp:
        # Use spaCy if available
        doc = nlp(text)
        words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

        vectorizer = TfidfVectorizer(stop_words='english')
        tfIdf_matrix = vectorizer.fit_transform([" ".join(words)])
        feature_arr = vectorizer.get_feature_names_out()
        tfIdf_sorting = tfIdf_matrix.toarray().flatten().argsort()[::-1]
    else:
        # Fall back to simple TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', max_features=n)
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_arr = vectorizer.get_feature_names_out()
        tfIdf_sorting = tfidf_matrix.toarray().flatten().argsort()[::-1]

    return [feature_arr[i] for i in tfIdf_sorting[:n]]


# ----------------------------------------------
# Advanced Collaborative Filtering (Surprise)
# ----------------------------------------------
def get_collaborative_filtering_recommendations():
    user_ratings = BookRating.objects.all()

    if not user_ratings:
        return []
    
    # Check if we have enough ratings to do proper collaborative filtering
    if len(user_ratings) < 10:
        print("Not enough ratings for collaborative filtering")
        return []

    try:
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            pd.DataFrame(list(user_ratings.values("user__id", "book_id", "rating"))),
            reader
        )

        # Use a smaller test set if we don't have many ratings
        test_size = 0.2 if len(user_ratings) >= 20 else 0.1
        train_set, test_set = train_test_split(data, test_size=test_size)

        model = SVD()
        model.fit(train_set)

        predictions = model.test(test_set)

        book_predictions = {}
        for uid, iid, true_r, est, _ in predictions:
            if iid not in book_predictions:
                book_predictions[iid] = est
            else:
                book_predictions[iid] += est

        recommended_books = sorted(book_predictions.items(), key=lambda x: x[1], reverse=True)
        top_recommended_books = [fetch_books_from_google_api_using_id(book[0]) for book in recommended_books[:10]]

        return top_recommended_books
    except Exception as e:
        print(f"Error in collaborative filtering: {e}")
        return []


# -------------------------------------
# Rank by Embeddings using Hugging Face API
# -------------------------------------
def rank_books_by_cosine_similarity(media_query, books):
    if not books:
        return []
    
    book_descriptions = [book.get("description", "") for book in books]
    texts_to_embed = book_descriptions + [media_query["description"]]
    
    # Get all embeddings in one batch request
    print(f"Getting embeddings for {len(texts_to_embed)} texts...")
    all_embeddings = get_embeddings_batch(texts_to_embed)
    
    if not all_embeddings or len(all_embeddings) < len(texts_to_embed):
        print("Error getting embeddings, falling back to basic ranking")
        return books[:min(39, len(books))]
    
    # Split the embeddings
    book_embeddings = all_embeddings[:-1]
    media_embedding = all_embeddings[-1]
    
    # Calculate similarity scores
    similarity_scores = [cosine_similarity(media_embedding, book_emb) for book_emb in book_embeddings]
    
    # Zip books with their scores, sort, and return top books
    ranked_books = list(zip(books, similarity_scores))
    ranked_books.sort(key=lambda x: x[1], reverse=True)
    
    return [book[0] for book in ranked_books][:39]


# -------------------------------
# Final Recommendation Flow with Django Cache
# -------------------------------
def get_recommended_books(media_query):
    print(f"Getting recommendations for: {media_query.get('title', '')}")
    
    # Create a simplified cache key that's more likely to match for similar queries
    # Only use title and genre for the cache key
    simplified_query = {
        'title': media_query.get('title', '').lower().strip(),
        'genre': media_query.get('genre', '').lower().strip()
    }
    
    # Generate a safer cache key using a hash of the simplified query
    query_string = f"{simplified_query['title']}:{simplified_query['genre']}"
    safe_key = hashlib.md5(query_string.encode()).hexdigest()
    cache_key = f"recommendations_{safe_key}"
    
    print(f"Cache key: {cache_key}")
    
    # Try to get cached recommendations
    cached_recommendations = cache.get(cache_key)
    if cached_recommendations:
        print("✅ CACHE HIT! Fetching recommendations from cache")
        return cached_recommendations
    else:
        print("❌ CACHE MISS! No cached recommendations found")

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
    cache.set(cache_key, ranked_book_recommendations, timeout=1800)
    print(f"✅ Successfully cached recommendations with key: {cache_key}")

    return ranked_book_recommendations
