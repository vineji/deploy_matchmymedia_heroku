import math
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from . import recommendation
import json
from rest_framework import status

import requests

import os
from dotenv import load_dotenv

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, get_user_model, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from .forms import CustomUserCreationForm, CustomUserUpdateForm

from .models import Genre, BookRating, FriendRequest, Friendship

from datetime import date
from django.utils.timezone import now
from datetime import timedelta

from django.core.paginator import Paginator, Page

from django.db.models import Q


load_dotenv()


def main_spa(request):
    return render(request, 'index.html')

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

def login_view(request):
    if request.method== "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(request.session.items())
            return redirect("/dashboard/")
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid username or password."})
    form = AuthenticationForm()
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, "login.html")

def sign_up_view(request):
    if request.method== "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect("/dashboard/")
        else:
            print(form.errors)
            return render(request, "signup.html", {"form": form})
    
    form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

@login_required
def user_view(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            user_data = request.user.to_dict()
            return JsonResponse(user_data)
        
    elif request.method == "PUT":

        data = json.loads(request.body)
        action = data.get('action')

        if not action:

            try:
                User = request.user

                updated_data = {
                    "username": data.get("username", User.username),
                    "online_id": data.get("online_id", User.online_id),
                    "email": data.get("email", User.email),
                    "DOB": data.get("DOB", User.DOB)
                }
                form  = CustomUserUpdateForm(updated_data, instance=request.user)
                if form.is_valid():
                    form.save()
                    return JsonResponse({"message": "User details updated successfully!"})
                else:
                    print(form.errors)
                    return JsonResponse({"errors": form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data."}, status=400)
    
    elif request.method == "POST":

        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'change_password':
            try:
                form = PasswordChangeForm(user=request.user, data = data)

                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return JsonResponse({"message": "Password updated successfully!"})
                else:
                    print(form.errors)
                    return JsonResponse({"errors": form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data."}, status=400)
        
        elif action == 'add_genre':

            try:
                genre_name = data.get('genre_name')

                if not genre_name:
                    return JsonResponse({"error": "Genre name is required"}, status=400)
                
                genre = Genre.objects.get(name=genre_name)

                request.user.favourite_genres.add(genre)
                request.user.save()

                return JsonResponse({"message": "Genre added successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        
        elif action == 'add_book':

            try:
                book = data.get('book')

                if not book:
                    return JsonResponse({"error": "Book is required"}, status=400)
                
                if book in request.user.favourite_books:
                    return JsonResponse({"error": "Book is already added to favourites"}, status=400)

                request.user.favourite_books.append(book)
                request.user.save()

                return JsonResponse({"message": "Book added successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    
    elif request.method == 'DELETE':

        data = json.loads(request.body)
        action = data.get('action')

        
        if action == 'delete_genre':

            try:
                genre_name = data.get('genre_name')

                if not genre_name:
                    return JsonResponse({"error": "Genre name is required"}, status=400)
                
                genre = Genre.objects.get(name=genre_name)

                request.user.favourite_genres.remove(genre)
                request.user.save()

                return JsonResponse({"message": "Genre removed successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        elif action == "delete_book":

            try:
                book = data.get('book')

                if not book:
                    return JsonResponse({"error": "Book is required"}, status=400)
                
                if book not in request.user.favourite_books:
                    return JsonResponse({"error": "Book is already deleted to favourites"}, status=400)

                request.user.favourite_books.remove(book)
                request.user.save()

                return JsonResponse({"message": "Book deleted successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def user_list_view(request):

    if request.method == "GET":

        sort = request.GET.get("sort", "Most Common")
        min_age = request.GET.get("minAge")
        max_age = request.GET.get("maxAge")

        all_users = get_user_model().objects.exclude(id = request.user.id)

        today = now().date()

        if min_age:
            min_age_date = today - timedelta(days=int(min_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB <= min_age_date]
        if max_age:
            max_age_date = today - timedelta(days=int(max_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB >= max_age_date]
        
        if not min_age and not max_age:
            all_users = list(all_users)


        logged_user_genres = set(request.user.favourite_genres.all())

        def get_common_genre_count(user):
            user_genres = set(user.favourite_genres.all())
            return len(logged_user_genres & user_genres)
        
        for i in range(len(all_users)):
            for j in range(i + 1, len(all_users)):
                if get_common_genre_count(all_users[j]) > get_common_genre_count(all_users[i]):
                    user = all_users[i]
                    all_users[i] = all_users[j]
                    all_users[j] = user


        if sort == "Least Common":
            all_users = all_users[::-1]
        
        page_number = request.GET.get('page', 1)
        paginator = Paginator(all_users, 5)
        page_object = paginator.get_page(page_number)

        friend_ids= set(Friendship.objects.filter(user=request.user).values_list('friend_id', flat=True))

        final_all_users = []

        for user in page_object:
            if user.id in friend_ids:
                final_all_users.append(user.user_list_friend_to_dict())
            else:
                final_all_users.append(user.user_list_to_dict())


        response_data = {
            "user_list" : final_all_users,
            'total_pages': paginator.num_pages,
            'current_page': page_object.number,
            'has_next': page_object.has_next(),
            'has_previous': page_object.has_previous(),
        }

        return JsonResponse(response_data)

@login_required
def genre_view(request):

    if request.method == "GET":

        all_genres = Genre.objects.all()
        genre_list = [[genre.name,genre.colour] for genre in all_genres]

        return JsonResponse(genre_list, safe=False)
    
    elif request.method == "POST":
        try:

            data = json.loads(request.body)
            genre_name = data.get('genre_name')

            if not genre_name:
                return JsonResponse({"error": "Genre name is required"}, status=400)
            
            genre_name_cleaned = genre_name.strip().lower()

            genre = Genre.objects.filter(name__iexact=genre_name_cleaned).first()


            if genre:
                return JsonResponse({"message": "Genre already exists.","genre_name": genre.name,}, status=201)
            
            genre = Genre.objects.create(name=genre_name)

            return JsonResponse({
                "message": "Genre added to the database successfully.",
                "genre_name": genre.name,
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def book_rating_view(request):


    if request.method == "GET":
        book_id = request.GET.get('book_id')

        book_rating = BookRating.objects.filter(
            user = request.user,
            book_id = book_id,
        ).first()

        if book_rating:
            return JsonResponse({"book_rating" : book_rating.rating}, status=201)
        else:
            return JsonResponse({"book_rating" : 0}, status=201)


    elif request.method == "POST":

        data = json.loads(request.body)
        book_id = data.get('book_id')
        rating = float(data.get('book_rating'))
        
        book_rating = BookRating.objects.filter(
            user = request.user,
            book_id = book_id,
        ).first()

        if book_rating:
            book_rating.rating = rating
            book_rating.save()
        else:
            book_rating = BookRating.objects.create(
            user = request.user,
            book_id = book_id,
            rating = rating
        )
        
        return JsonResponse({'message': 'Book rating added/updated successfully'})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


def movie_search_view(request):
    
    if request.method == 'GET':

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)
        api_key = os.getenv("TMBD_API_KEY")

        if not title:
            url = f'https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}&page={page_number}'
        else:
            url = f'https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&page={page_number}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data['results']
            total_pages = data['total_pages']
            current_page = data['page']
            response_data = {
                'movies': movies,
                'total_pages': total_pages,
                'current_page': current_page,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'movies':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def show_search_view(request):
        
    if request.method == 'GET':

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)
        api_key = os.getenv("TMBD_API_KEY")

        if not title:
            url = f'https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}&page={page_number}'
        else: 
            url = f'https://api.themoviedb.org/3/search/tv?query={title}&api_key={api_key}&page={page_number}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            tv_shows = data['results']
            total_pages = data['total_pages']
            current_page = data['page']
            response_data = {
                'shows': tv_shows,
                'total_pages': total_pages,
                'current_page': current_page,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'shows':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def book_search_view(request):
        
    if request.method == 'GET':

        title = request.GET.get('title', '')
        page_number = request.GET.get('page', 1)
        maxItemsPerPage = 20
        startIndex = maxItemsPerPage * (int(page_number) - 1)

        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

        if not title:
            url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=Relevance&startIndex={startIndex}&maxResults={maxItemsPerPage}&key={api_key}'
        else:
            url = f'https://www.googleapis.com/books/v1/volumes?q={title}&startIndex={startIndex}&maxResults={maxItemsPerPage}&key={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            books = data.get('items', [])
            total_items = data.get('totalItems', 0)
            total_pages = math.ceil(total_items / maxItemsPerPage) if books else 0
            current_page = page_number

            response_data = {
                'books': books,
                'total_pages': total_pages,
                'current_page': current_page
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'books':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_book_recommendations_view(request):
        
    if request.method == 'GET':
        data = request.GET.dict()

        recommendations = recommendation.get_recommended_books(data) 

        return JsonResponse({"recommendations": recommendations})


@login_required
def friend_request_view(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            from_user = request.user
            to_user_id = data.get("friend_id")
            to_user = get_user_model().objects.get(id = to_user_id)

            existing_request= FriendRequest.objects.filter(Q(from_user = from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)).first()

            if existing_request:
                if existing_request.status == "pending":
                    return JsonResponse({"message" : "There is already a pending request between you two"})
                elif existing_request.status == "declined":
                    return JsonResponse({"message" : "Friend request was declined between you two"})

            
            FriendRequest.objects.create(from_user = from_user, to_user = to_user)
            return JsonResponse({"message" : "Friend Request Sent"})
            
        except get_user_model().DoesNotExist:
            return JsonResponse({"message" : " User Does Not Exists"}, status = 404)
        
        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 500)
    
    elif request.method == "GET":

        friend_request_recieved_list = FriendRequest.objects.filter(to_user = request.user)
        friend_request_sent_list = FriendRequest.objects.filter(from_user = request.user)

        friend_request_list = []

        for x in friend_request_recieved_list:
            friend_request_list.append(x.to_dict_recieved())
        
        for x in friend_request_sent_list:
            friend_request_list.append(x.to_dict_sent())


        return JsonResponse(friend_request_list, safe=False)
    
    elif request.method == "PUT":

        data = json.loads(request.body)

        action = data.get("action")

        if action == "accept":

            try:

                friend_request_id = data.get("request_id")

                friend_request = FriendRequest.objects.filter(id = friend_request_id, to_user = request.user).first()

                friend_request.status = "accepted"
                friend_request.save()

                from_user = friend_request.from_user

                try:
                    Friendship.objects.create(user=from_user, friend=request.user)
                    Friendship.objects.create(user=request.user, friend=from_user)

                except IntegrityError:
                    return JsonResponse({"message" : "Friendship already exists"})

                return JsonResponse({"message" : "Friend request accepted"})
                    
            except get_user_model().DoesNotExist:
                return JsonResponse({"message" : " User Does Not Exists"}, status = 404)
            
        elif action == "decline":
            try:

                friend_request_id = data.get("request_id")

                friend_request = FriendRequest.objects.filter(id = friend_request_id, to_user = request.user).first()

                friend_request.status = "declined"
                friend_request.save()

                return JsonResponse({"message" : "Friend request declined"})
            
            except get_user_model().DoesNotExist:
                return JsonResponse({"message" : " User Does Not Exists"}, status = 404)



@login_required
def friendship_view(request):

    if request.method== "GET":

        friendship_list = Friendship.objects.filter(user = request.user)

        friendship_list = [x.get_friend() for x in friendship_list]

        return JsonResponse(friendship_list, safe=False)







