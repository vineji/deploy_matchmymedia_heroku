<template>
    <div class="search_container">
        <form @submit.prevent class="search">
            <div class="search_button_div">
                <button @click="toggleMedia('Books')"
                :class="{active: searchMedia === 'Books'}"
                class="book_button"
                > Books</button>
                <button @click="toggleMedia('Movies')"
                :class="{active: searchMedia === 'Movies'}"
                class="movie_button"
                > Movies </button>

                <button @click="toggleMedia('TV Shows')"
                :class="{active: searchMedia === 'TV Shows'}"
                class="show_button"
                > TV Shows  </button>
            </div>
            <div class="searchbar">
                <input
                type="text"
                :placeholder="'Search ' + searchMedia + ' - Trending '+ searchMedia"
                v-model="query"
                @input="search(true)"
                />
                <button @click="clearQuery" class="clear_button">&times;</button>
            </div>
            <button class="rcmnd-button" @click="recommendBooks(chosenMedia)" >Recommend Books</button>
            <button class="login-btn" @click="redirectToLogin">{{loggedUser.online_id || 'Login'}}</button>
        </form>
        <RecommendModal
        v-model:isVisible="isModalVisible"
        :recommendedBooks="rcmndBooks"
        :mediaType="searchMedia"
        :mediaName="query"
        :loggedUser="loggedUser.online_id"
        @close="isModalVisible = false"
        />
        <div v-if="mediaList.length == 0 && isLoading == false && searchMedia == 'Books' && chosenMedia == null" class="no_more_books">
            <p>No more book results</p>
            <button @click="search(true)">Go Back</button>
        </div>
        <div v-if="mediaList.length > 0" class="media_list">
            <ul class="media_list_ul">
                <li class="media_list_li" v-for="media in mediaList" :key="media.id">
                    <img v-if="this.searchMedia == 'Movies' || this.searchMedia == 'TV Shows'" :src=" 'https://image.tmdb.org/t/p/original/' + media.poster_path" alt="Movie poster" class="list_img"  />
                    <img v-if="this.searchMedia == 'Books'" :src="media.volumeInfo?.imageLinks?.thumbnail" class="list_img">
                    <div class="sub_media_list">
                        <ul class="sub_media_list_ul" v-if="this.searchMedia == 'Movies' || this.searchMedia == 'TV Shows'">
                            <li><b>Title: </b>{{ media.title || media.name || "Title unavailable"}}</li>
                            <li><b>Released: </b>{{media.release_date || media.first_air_date || "Not specified"}}</li>
                            <li><b>Genres: </b></li>
                            <ul v-if="media.genre_ids?.length > 0" class="genre_list">
                                <li class="genre" v-for="id in media.genre_ids" :key="id" :style="{backgroundColor: getGenreColor(id)}"> {{ getGenreName(id) }}</li>
                            </ul>
                            <ul v-else class="genre_list">
                                <li class="genre" style="background-color: #9b9a9a;">Unknown</li>
                            </ul>
                        </ul>
                        <ul class="sub_media_list_ul" v-else-if="this.searchMedia == 'Books'" >
                            <li class="book_title"><b>Title: </b>{{ media?.volumeInfo?.title || 'No title available'}}</li>
                            <li><b>Published: </b>{{media?.volumeInfo?.publishedDate || "Not specified"}}</li>
                            <li><b>Categories: </b></li>
                            <ul v-if="media.volumeInfo?.categories?.length > 0"  class="genre_list">
                                <li class="genre" style="background-color: grey;" v-for="category in media.volumeInfo['categories']" :key="category">{{ category }}</li>
                            </ul>
                            <ul v-else class="genre_list">
                                <li class="genre" style="background-color: #9b9a9a;">Unknown</li>
                            </ul>
                        </ul>
                        <button @click="select(media)" class="media_list_button"> Select </button>
                    </div>
                </li>
            </ul>
            <li class="pagination_control">
                <button class="pagination_control_button_next_prev" :disabled="this.currentPage == 1" @click="prevPage">&lt;</button>
                <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page1 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page1 ? 'bold' : ''}" :disabled="page1 > totalPages" @click="changePage(page1)">{{page1}}</button>
                <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page2 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page2 ? 'bold' : ''}" :disabled="page2 > totalPages" @click="changePage(page2)">{{page2}}</button>
                <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page3 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page3 ? 'bold' : ''}" :disabled="page3 > totalPages" @click="changePage(page3)">{{page3}}</button>
                <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page4 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page4 ? 'bold' : ''}" :disabled="page4 > totalPages" @click="changePage(page4)">{{page4}}</button>
                <button class="pagination_control_button_next_prev" :disabled="this.currentPage >= totalPages" @click="nextPage">&gt;</button>
            </li>
        </div>
        <div v-if="this.show_ChosenMedia == true && (this.searchMedia == 'Movies' || this.searchMedia == 'TV Shows')" class="chosen_media">
            <img class="chosen_media_img" :src=" 'https://image.tmdb.org/t/p/original/' + chosenMedia.poster_path" alt="Movie poster"  />
            <div class="chosen_media_info">
                <p><b>Title: </b>{{ chosenMedia.title || chosenMedia.name}}</p>
                <p><b>Released: </b> {{chosenMedia.release_date || chosenMedia.first_air_date || "Unavailable" }}</p>
                <ul class="chosen_genre_list">
                    <p><b>Genres: </b> </p>
                    <li v-if="chosenMedia?.genre_ids?.length == 0" class="chosen_genre" style="grey">Unknown</li>
                    <li class="chosen_genre" :style="{backgroundColor: getGenreColor(id)}" v-for="id in chosenMedia.genre_ids" :key="id">{{ getGenreName(id) }}</li>
                </ul>
                <p class="overview"><b>Overview: </b> {{ chosenMedia.overview || "Description unavailable" }} </p>
            </div>
        </div>
        <div v-if="this.show_ChosenMedia == true && (this.searchMedia == 'Books')" class="chosen_media">
            <img class="chosen_media_img" :src="chosenMedia.volumeInfo?.imageLinks?.thumbnail" alt="Movie poster"  />
            <div class="chosen_media_info">
                <div class="chosen_media_title_div">
                    <p class="chosen_media_info_title"><b>Title: </b>{{ chosenMedia.volumeInfo['title'] || "Title unavailable"}}</p>
                    <button class="fav_btn" @click="addToFavourites(chosenMedia)">Add to Favourites</button>
                </div>
                <div class="chosen_author_div">
                    <ul class="authors">
                        <p><b>Authors: </b></p>
                        <li v-for="(author,index) in chosenMedia.volumeInfo?.authors" :key="index">
                            <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                        </li>
                    </ul>
                    <div class="star_rating_div">
                        <p>Your rating: </p>
                        <button
                        v-for="star in stars"
                        :key="star"
                        @click="rateBook(star)"
                        @mouseover="hoverStar(star)"
                        @mouseleave="resetHover"
                        :class="['star',{hovered: hoveredStar >= star, filled: rating >= star}]"
                        >
                        <span v-html="hoveredStar >= star || rating >= star ? '&#9733;' : '&#9734;'"></span>
                        </button>
                    </div>
                </div>
                <p><b>Published Date: </b> {{ chosenMedia.volumeInfo['publishedDate']|| "Not specified" }}</p>
                <ul v-if="chosenMedia.volumeInfo?.categories?.length > 0" class="chosen_genre_list">
                    <p><b>Categories: </b> </p>
                    <p v-if="chosenMedia.volumeInfo?.categories?.length == 0" class="chosen_genre" style="background-color: grey;" >Unknown</p>
                    <li class="chosen_genre" style="background-color: grey;" v-for="category in chosenMedia.volumeInfo?.categories" :key="category">{{ category }}</li>
                </ul>
                <ul v-else class="chosen_genre_list">
                    <p><b>Categories: </b> </p>
                    <li class="chosen_genre" style="background-color: #9b9a9a;">Unknown</li>
                </ul>
                <p class="overview"><b>Description: </b> {{ chosenMedia.volumeInfo['description'] || "Description unavailable" }}</p>
            </div>
        </div>
    </div>
</template>
<script>
import { useGenreStore } from '@/stores/genreStore';
import RecommendModal from './RecommendModal.vue';
import { useUserStore } from '@/stores/userStore';

export default {
    components: {RecommendModal},
    data() {
        return {
            query : '',
            mediaList : [],
            searchMedia : 'Movies',
            show_ChosenMedia : false,
            chosenMedia : null,
            currentPage : 1,
            totalPages : 1,
            showPageMultiplier : 1,
            isModalVisible : false,
            rcmndBooks : [],
            csrfToken : '',
            stars : [1,2,3,4,5],
            rating : 0,
            hoveredStar : 0,
            isLoading : false,
        };
    },
    setup(){
        const userStore = useUserStore();
        userStore.loadUser();
        return {userStore};
    },
    computed: {
        genreStore(){
            return useGenreStore();
        },
        loggedUser(){
            return{
                id: this.userStore.user_id || null,
                online_id: this.userStore.online_id || null,
                favourite_genres: this.userStore.favourite_genres || [],
            }
        },
        page1(){
            return (4 * this.showPageMultiplier) - 3
        },
        page2(){
            return (4 * this.showPageMultiplier) - 2
        },
        page3(){
            return (4 * this.showPageMultiplier) - 1
        },
        page4(){
            return (4 * this.showPageMultiplier)
        },
    },
    methods: {

        async fetch_csrf_token(){

            try{
                const response = await fetch("http://127.0.0.1:8000/csrf/",
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.csrfToken = data.csrfToken;
                    console.log(`Fetched csrf token: ${this.csrfToken}`);
                }
                else{
                console.log(`Failed to fetch token, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching token, ${error}`)
            }
        },
        async search(newSearch){
            this.isLoading = true;

            this.show_ChosenMedia = false;
            this.chosenMedia = null;


            if (newSearch == true){
                this.currentPage = 1;
                this.showPageMultiplier = 1;
            }
            

            if (this.searchMedia == "Movies"){
                try{
                    const response = await fetch(`http://127.0.0.1:8000/search-movie/?title=${this.query}&page=${this.currentPage}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.mediaList = data.movies || [];
                    this.currentPage = data.current_page || 1;
                    this.totalPages = data.total_pages || 1;
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
            else if (this.searchMedia == "TV Shows"){
                try{
                    const response = await fetch(`http://127.0.0.1:8000/search-show/?title=${this.query}&page=${this.currentPage}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.mediaList = data.shows || [];
                    this.currentPage = data.current_page || 1;
                    this.totalPages = data.total_pages || 1;
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
            else if (this.searchMedia == "Books"){
                try{
                    const response = await fetch(`http://127.0.0.1:8000/search-book/?title=${this.query}&page=${this.currentPage}`);
                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.mediaList = data.books || [];
                    this.currentPage = data.current_page || 1;
                    this.totalPages = data.total_pages || 1;
                    console.log(data);
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
            this.isLoading = false;

        },
        async recommendBooks(media){

            if (media == null){
                alert("Select a media in order to get book recommendations.");
                return;
            }
            this.rcmndBooks = [];
            this.openModal();

            let media_map = new Map();
            let genres = []

            if (this.searchMedia == "Movies" || this.searchMedia == "TV Shows"){
                for (let i = 0; i < media.genre_ids.length; i++){
                    genres.push(this.getGenreName(media.genre_ids[i]))
                }
                media_map.set("title", media.title || media.name);
                media_map.set("description", media.overview);
                media_map.set("genre", genres);
            }
            else if(this.searchMedia == "Books"){
                media_map.set("title", media.volumeInfo['title']);
                media_map.set("description",media.volumeInfo['description']);
                media_map.set("genre", media.volumeInfo['categories']);
            }

            let media_params = new URLSearchParams(media_map)

            let url = 'http://127.0.0.1:8000/get-recommendations/?' + media_params.toString();
            try {
                const response = await fetch(url);

                if(!response.ok){
                    throw new Error("Failed to fecth recommendations");
                }
                const data = await response.json();
                this.rcmndBooks = data.recommendations || [];
            }
            catch (error){
                console.error("Error fecthing recommendations ", error)
            }
        },
        async addToFavourites(book){
            if (this.loggedUser.online_id){
                const book_object = {}
                book_object.id = book.id;
                book_object.image = book.volumeInfo?.imageLinks?.thumbnail;
                book_object.title = book.volumeInfo?.title;
                book_object.authors = book.volumeInfo?.authors;
                book_object.published_date = book.volumeInfo['publishedDate']|| "Not specified";
                book_object.categories = book.volumeInfo?.categories;
                book_object.description = book.volumeInfo?.description;

                try
                {
                    const response = await fetch("http://127.0.0.1:8000/user/",
                    {    
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": this.csrfToken,
                        },
                        body: JSON.stringify({ book: book_object, action: "add_book" }),
                        credentials: "include", 
                    })
                    const data = await response.json();
                    if (!response.ok) {
                        if (data.error === 'Book is already added to favourites'){

                            alert("You have already added this book to your favourites");
                        }
                        else{
                            throw new Error(`Failed to add book: ${response.status}`);
                        }
                    }
                }
                catch (error){
                    console.error("Error adding book:", error);
                }
            }
            else{
                alert("You have to login to favourite a book.");
            }

        },
        async fetch_book_rating(){
            if (this.loggedUser.online_id && this.searchMedia == "Books"){
                try
                {
                    const response = await fetch(`http://127.0.0.1:8000/book-rating/?book_id=${this.chosenMedia.id}`,
                    {    
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": this.csrfToken,
                        },
                        credentials: "include", 
                    })
                    if (!response.ok) {
                        throw new Error(`Failed to fetch book: ${response.status}`);
                    }
                    const data = await response.json();
                    this.rating = data.book_rating || 0;
                }
                catch (error){
                    console.error("Error fetching book:", error);
                }

            }
        },
        async rateBook(rating){

            if (this.loggedUser.online_id){
                this.rating = rating;
                try
                {
                    const response = await fetch("http://127.0.0.1:8000/book-rating/",
                    {    
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": this.csrfToken,
                        },
                        body: JSON.stringify({ book_id: this.chosenMedia?.id, book_rating: rating }),
                        credentials: "include", 
                    })
                    if (!response.ok) {
                            throw new Error(`Failed to add book: ${response.status}`);
                        }
                }
                catch (error){
                    console.error("Error adding book:", error);
                }

            }
            else{
                alert("You need to login to rate a book");
            }

        },
        hoverStar(star){
            this.hoveredStar= star;
        },
        resetHover(){
            this.hoveredStar = 0;
        },
        openModal(){
            this.isModalVisible =  true;
        },
        toggleMedia(media){
            this.currentPage = 1;
            this.showPageMultiplier = 1;
            this.show_ChosenMedia = false;
            this.searchMedia = media;
            this.mediaList = [];
            this.search(true);
        },
        clearQuery(){
            this.currentPage = 1;
            this.query = '';
            this.mediaList = [];
            this.chosenMedia = null;
            this.show_ChosenMedia = false;
            this.search(true);
        },
        select(media){
            this.show_ChosenMedia = true;
            this.chosenMedia = media;
            this.fetch_book_rating();
            this.mediaList = [];
            this.query = media.title || media.name || media.volumeInfo['title'];
            this.currentPage = 1;
        },
        getGenreName(id){
            return this.genreStore.getGenreById(id);

        },
        getGenreColor(id){
            return this.genreStore.getGenreColorById(id);
        },
        changePage(pageNumber){
            this.currentPage = pageNumber;
            this.search(false);
            window.scrollTo({top: 0, behavior: 'smooth'});
        },
        nextPage(){
            if (this.currentPage < this.totalPages){
                this.currentPage++;

                if (this.currentPage > this.page4){
                    this.showPageMultiplier++;
                }
                this.search(false);
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        },
        prevPage(){
            if (this.page1 == this.currentPage){
                this.showPageMultiplier--;
                this.changePage(this.page4);
            }
            else{
                this.changePage(Number(this.currentPage)-1)
            }
            this.search(false);
            window.scrollTo({top: 0, behavior: 'smooth'});
        },
        redirectToLogin(){
            if (this.loggedUser.online_id){
                window.location.href= "/dashboard/";
            }
            else{
                window.location.href= "http://127.0.0.1:8000/login/";
            }
        }
    },
    mounted(){
        this.search(true);
        this.fetch_csrf_token();
    }
    
    };
</script>
<style>

body{
    background-color: #f7f7f7;
}

li{
    list-style: none;
}
.search_container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.search{
    display: flex;
    flex-direction: row;
    gap: 1rem;
}
.no_more_books{
    margin-top: 2rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 26rem;
    justify-content: space-between;
}
.no_more_books p{
    border-radius: 0.8rem;
    background: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 1.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.7rem;
    padding-bottom: 0.7rem;
}
.no_more_books button{
    all: unset;
    background-color: #e51635;
    color: #FBFFFE;
    font-weight: 400;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-right: 1rem;
    padding-left: 1rem;
    height: 2.4rem;
    font-size: 1.5rem;
    border-radius: 0.8rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.no_more_books button:hover{
    background-color: #e51635c5;

}
.searchbar {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 32rem;
    height: 3rem;
    border-radius: 0.8rem;
    font-size: 1.2rem;
    border: #1B1B1E solid 3px;
    border-right: none;
    color: #6D676E;
    background-color: #FBFFFE;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.searchbar input{
    width: 28rem;
    height: 2.8rem;
    border-radius: 1rem;
    font-size: 1.2rem;
    border: none;
    padding-left: 1rem;
    outline: none;

}

.search_button_div{
    background-color: #FBFFFE;
    border: #FAA916 solid 3px;
    height: 3rem;
    border-radius: 0.8rem;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.book_button{
    all: unset;
    background-color: #FBFFFE;
    color: #FAA916;
    height: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
    cursor: pointer;
    font-weight: 500;
    font-size: 1.2rem;
}

.movie_button{
    all: unset;
    background-color: #FBFFFE;
    color: #FAA916;
    height: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
    cursor: pointer;
    font-weight: 500;
    font-size: 1.2rem;
    border-right: 3px #FAA916 solid;
    border-left: 3px #FAA916 solid;
}
.show_button{
    all: unset;
    background-color: #FBFFFE;
    color: #FAA916;
    height: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
    cursor: pointer;
    font-weight: 500;
    font-size: 1.2rem;
}
.rcmnd-button{
    all: unset;
    font-size: 1.15rem;
    background-color: #41ceaa;
    padding-left: 1rem;
    padding-right: 1rem;
    font-weight: 451;
    color: #1B1B1E;
    border-radius: 0.8rem;
    height: 3.31rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}


.rcmnd-button:hover{
    background-color: #25c79eb5;
    color: #1b1b1e8f;
    transition: 0.3s ease;
}
.login-btn{
    all: unset;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.15rem;
    background-color: #FBFFFE;
    padding-left: 1rem;
    padding-right: 1rem;
    font-weight: 500;
    color: #1B1B1E;
    border-radius: 0.8rem;
    border: 3px solid #1B1B1E;
    height: 3rem;
    transition: 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.login-btn:hover{
    background-color: #1B1B1E;
    color: #FBFFFE;
    transition: 0.3s ease;
}


.search_button_div button.active{
    background-color: #FAA916;
    color: #FBFFFE;
}
.clear_button{
    all: unset;
    font-weight: 500;
    font-size: 2rem;
    width: 3.5rem;
    border-radius: 0.8rem;
    height: 3.4rem;
    color: #FBFFFE;
    background-color: #e51635;
}
.clear_button:hover{
    font-weight: 600;
    background-color: #ff1538;
    transition: ease 0.3s;
}

.media_list{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 1rem;
}

.media_list_ul{
    display: flex;
    flex-direction: row;
    width: 88rem;
    max-width: 88rem;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 1.5rem;

}
.media_list_li {
    background-color: #FBFFFE;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 19rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    min-height: 13rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    transition: 0.3s ease;
}
.media_list_li:hover {
    transform: scale(1.06);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.media_list_button{
    margin-top: 1rem;
    width: 9rem;
    min-height: 1.5rem;
    height: 1.5rem;
    max-height: 1.5rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    transition: 0.2s ease;

}
.media_list_button:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.sub_media_list{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    height: 12rem;
    
    
}
.sub_media_list_ul{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 9rem;
    max-width: 9rem;
    height: 10rem;
    text-align: left;
    gap: 0.3rem;
    padding: 0;
    margin: 0;
}
.book_title{
    max-height: 5rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    width: 9.1rem;
    padding-right: 0.1rem;
}
.book_title::-webkit-scrollbar{
    width: 3px;
}

.book_title::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.book_title::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}

.pagination_control{
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
    border-radius: 1rem;
    height: 6rem;
    max-height: 6rem;
    gap: 0.5rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
    width: 33rem;
    margin-left: 2.5rem;
}
.pagination_control_button_page{
    height: 4.8rem;
    width: 4.8rem;
    font-size: 2rem;
    border: #1B1B1E 3px solid;
    background-color: #ffffff;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    border-radius: 0.8rem;
    transition: transform 0.2s ease, box-shadow0.2s ease;
}
.pagination_control_button_next_prev{
    height: 3.5rem;
    width: 3.5rem;
    font-size: 2rem;
    border: #1B1B1E 3px solid;
    background-color: #ffffff;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    border-radius: 0.8rem;
    transition: transform 0.2s ease, box-shadow0.2s ease;

}
.pagination_control_button_page:disabled{
    border: #b8b7b7 3px solid;
    color: #b8b7b7;
    
}
.pagination_control_button_page:disabled:hover{
    background-color: #ffffff;
    transform: scale(1.0);
    font-weight: normal;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.pagination_control_button_page:hover{
    background-color: #41ceaa;
    font-weight: bold;
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
.pagination_control_button_next_prev:disabled{
    border: #b8b7b7 3px solid;
    color: #b8b7b7;
    
}
.pagination_control_button_next_prev:disabled:hover{
    background-color: #ffffff;
    transform: scale(1.0);
    font-weight: normal;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.pagination_control_button_next_prev:hover{
    background-color: #41ceaa;
    font-weight: bold;
    transform: scale(1.1);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}



.genre_list{
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem;
    justify-content: flex-start;
    align-items: flex-start;
    width: 9.2rem;
    max-width: 9.2rem;
    padding: 0;
    margin: 0;
    font-size: 0.8rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}

.genre_list::-webkit-scrollbar{
    width: 3px;
}

.genre_list::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.genre_list::-webkit-scrollbar-track{
    background-color: #dcdcdc;
}

.genre{
    display: inline-block;
    color: #FBFFFE;
    padding-right: 0.4rem;
    padding-left: 0.4rem;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    border-radius: 0.3rem;
    max-width: 8rem;
    
}

.list_img{
    height: auto;
    width: 8rem;
    max-width: 100%;
    border-radius: 0.39rem;
}

.chosen_media{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 3rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    background-color: #FBFFFE;
    width: 53rem;
    margin-right: 5rem;
    margin-top: 2rem;
    padding: 2rem;
}

.chosen_media_img{
    align-self: flex-start;
    height: auto;
    width: 9rem;
    max-width: 100%;
    border-radius: 0.3rem;
}


.chosen_media_info{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-evenly;
    width: 40rem;
    min-height: 14rem;

}
.chosen_media_title_div{
    display: flex;
    flex-direction: row;
    width: 100%;
    align-items: flex-start;
    justify-content: space-between;
}
.fav_btn{
    all: unset;
    font-size: 1rem;
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #41ceaa;
    background-color: #FBFFFE;
    border: solid 3px #41ceaa;
    font-weight: 501;
    border-radius: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.2s ease;
}
.fav_btn:hover{
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.chosen_media_info p{
    gap: 0;
    margin: 0;
    text-align: left;
}
.chosen_media_info_title{
    width: 30rem;
    max-width: 30rem;
}
.chosen_genre_list{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
    width: 40rem;
    max-width: 40rem;
    padding: 0;
    gap: 0.5rem;
    margin-top: 1rem;
}
.chosen_genre{
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
    border-radius: 0.5rem;
    color: white;
}
.chosen_author_div{
    margin: 0;
    padding: 0;
    margin-top: 0.2rem;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
.authors{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
    width: 25rem;
    max-width: 25rem;
    padding: 0;
    gap: 0.5rem;
}
.star_rating_div{
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 14rem;
}
.star_rating_div p{
    font-size: 1rem;
    margin-right: 0.5rem;
    font-weight: 501;
}
.star{
    all: unset;
    background: none;
    border: none;
    font-size: 1.5rem;
    font-weight: 601;
    cursor: pointer;
    color: #FAA916;
}
.star:hover{
    color: #FAA916;
}
.star.filled{
    color: #FAA916;
}




</style>