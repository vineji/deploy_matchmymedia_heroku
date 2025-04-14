import requests
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from .models import BookRating
import os
from dotenv import load_dotenv

import redis
import json

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
load_dotenv()


nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_books_from_google_api(query):
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    recommendations = []

    start_index = 0
    
    max_results = 40
    
    filtered_categories = ["fiction", "drama", "adventure", "fantasy", "horror", "action", "comedy", "history", "western"
                           , "crime", "mystery", "romance", "magic", "family", "war", "kids", "children", "sci-fi", "comic", "novel", "graphic"]

    try:

        while len(recommendations) < max_results:

            url = "https://www.googleapis.com/books/v1/volumes"
            
            query_string = f"{query['keywords']} {query['genre']}"
            query_string_title = f"{query['title']}"

            

            param_list = {
                "q" : query_string,
                "maxResults" : 40,
                "startIndex" : start_index,
                "key" : api_key
            }

            param_list_title = {
                "q" : query_string_title,
                "maxResults" : 5,
                "startIndex" : start_index,
                "key" : api_key
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
                    "id" : book.get("id"),
                    "title" : volumeInfo.get("title", "Unknown Title"),
                    "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date" : volumeInfo.get("publishedDate", "Unknown"),
                    "description" : volumeInfo.get("description", "No Description Available"),
                    "categories" : categories,
                    "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
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
                    "id" : book.get("id"),
                    "title" : volumeInfo.get("title", "Unknown Title"),
                    "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date" : volumeInfo.get("publishedDate", "Unknown"),
                    "description" : volumeInfo.get("description", "No Description Available"),
                    "categories" : categories,
                    "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
                })
            
            start_index += len(books_data.get("items", []))
            if len(books_data.get("items", [])) < 40:
                    break
        
        dupe_title_date = set()
        final_recommendations = []

        for book in recommendations:
            if (book["title"],book["published_date"]) not in dupe_title_date:
                final_recommendations.append(book)
                dupe_title_date.add((book["title"],book["published_date"]))
            
        return final_recommendations
    
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []


def extract_keywords(text, n=7):
    
    doc = nlp(text)
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfIdf_matrix = vectorizer.fit_transform([" ".join(words)])
    feature_arr = vectorizer.get_feature_names_out()
    tfIdf_sorting = tfIdf_matrix.toarray().flatten().argsort()[::-1]


    return [feature_arr[i] for i in tfIdf_sorting[:n]]


def fetch_books_from_google_api_using_id(id):
        

        
    url = f"https://www.googleapis.com/books/v1/volumes/{id}"

    response = requests.get(url)

    response.raise_for_status()
    book_data = response.json()
    
    volumeInfo = book_data.get("volumeInfo", {})
    categories = volumeInfo.get("categories", [])

    phrases_to_remove = ["<p>","</p>","<br>","</br>","<b>","</b>","<i>","</i>"]

    description = volumeInfo.get("description", "No Description Available")

    for x in phrases_to_remove:
        description = description.replace(x, "")

    return {
        "id" : book_data.get("id"),
        "title" : volumeInfo.get("title", "Unknown Title"),
        "authors" : volumeInfo.get("authors", ["Unknown Author"]),
        "published_date" : volumeInfo.get("publishedDate", "Unknown"),
        "description" : description,
        "categories" : categories[:3],
        "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
    }




def get_collaborative_filtering_recommendations():

    user_ratings = BookRating.objects.all()

    if not user_ratings:
        return []
    
    print(user_ratings)

    reader = Reader(rating_scale=(1,5))

    data = Dataset.load_from_df(
        pd.DataFrame(list(user_ratings.values("user__id", "book_id", "rating"))),
        reader
    )

    train_set, test_set = train_test_split(data, test_size=0.2)

    model = SVD()
    model.fit(train_set)

    predictions = model.test(test_set)

    book_predictions = {}

    for uid, iid, true_r, est, _ in predictions:
        if iid not in book_predictions:
            book_predictions[iid] = est
        else:
            book_predictions[iid] += est
    
    
    recommended_books = sorted(book_predictions.items(), key=lambda x : x[1], reverse=True)


    top_recommended_books= [fetch_books_from_google_api_using_id(book[0]) for book in recommended_books[:10]]

    return top_recommended_books


def rank_books_by_cosine_similarity(media_query, books):

    book_descriptions = [book.get("description","") for book in books]

    book_embeddings = model.encode(book_descriptions, convert_to_tensor=True)
     
    media_embedding = model.encode(media_query["description"], convert_to_tensor=True)

    similarity_scores = util.pytorch_cos_sim(media_embedding, book_embeddings)

    similarity_scores = similarity_scores.squeeze(0).tolist()

    ranked_books = list(zip(books, similarity_scores))
    
    ranked_books.sort(key=lambda x: x[1], reverse=True)

    return [book[0] for book in ranked_books][:39]
    

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



                


