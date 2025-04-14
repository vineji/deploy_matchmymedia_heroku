<template>
    <div class="page_container">
        <h1>User Dashboard</h1>
        <router-link :to="{name: 'Main Page'}">Home</router-link>
        <button @click="logout">Logout</button>
        <router-link :to="{name: 'Social Page'}">Community</router-link>
        <div class="dashboard_container">   
            <div class="user_info">
                <h2 class="user_info_header">User Information</h2>
                <ul v-if="changePassword == false"  class="user_info_list">
                    <li class="user_info_li">
                        <p><b>Username</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_input" v-model="user_data.username" :placeholder="user_data.username" :readonly="readUsername" maxlength="15">
                            <button v-if="readUsername == true" class="change_btn" @click="changeUsername">Change</button>
                            <div class="change_div" v-else-if="readUsername == false">
                                <button @click="saveUsername" class="save_btn">Save</button>
                                <button @click="cancelUsername" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Online ID</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_input" v-model="user_data.online_id" :placeholder="user_data.online_id" :readonly="readOnlineId" maxlength="15">
                            <button v-if="readOnlineId == true" class="change_btn" @click="changeOnlineId">Change</button>
                            <div class="change_div" v-else-if="readOnlineId == false">
                                <button @click="saveOnlineId" class="save_btn">Save</button>
                                <button @click="cancelOnlineId" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Date of Birth</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_date" v-model="user_data.DOB" :placeholder="user_data.DOB" type="date" :readonly="readDOB" max="2020-01-01">
                            <button v-if="readDOB == true" class="change_btn" @click="changeDOB">Change</button>
                            <div class="change_div" v-else-if="readDOB == false">
                                <button @click="saveDOB" class="save_btn">Save</button>
                                <button @click="cancelDOB" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <button class="change_password_btn" @click="change_password">Change Password</button>
                </ul>
                <ul v-if="changePassword == true" class="user_info_list">
                    <li class="user_info_li">
                        <p><b>Old Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.old_password" placeholder="Enter Old Password" :type="showOldPassword ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_OldPassword">{{showOldPassword ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearOldPassword">Clear</button>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>New Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.new_password_1" placeholder="Enter New Password"  :type="showNewPassword1 ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_NewPassword1">{{showNewPassword1 ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearNewPassword1">Clear</button>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Confirm New Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.new_password_2" placeholder="Re-enter New Password" :type="showNewPassword2 ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_NewPassword2">{{showNewPassword2 ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearNewPassword2">Clear</button>
                        </div>
                    </li>
                    <div class="password_btn_div">
                        <button @click="updatePassword" class="update_btn">Update Password</button>
                        <button @click="cancelPassword" class="cancel_password_btn">Cancel</button>
                    </div>
                </ul>
            </div>   
            <div class="genre_book_container">
                <div class="add_genre_container">
                    <h3>Favourite Genres</h3>
                    <div class="genre_div">
                        <p>Your Genres:</p>
                        <button class="add_genre_btn" @click="openGenreModal">Add Genre</button>
                    </div>
                    <ul class="user_genre_list">
                        <li class="user_genre" style="background-color: grey;" v-if="user_data.favourite_genres.length == 0">No genres added yet</li>
                        <li v-for="genre in user_data.favourite_genres" :key="genre" class="user_genre" :style=" {backgroundColor: genre[1] } ">{{genre[0]}} <button class="delete_genre_btn" @click="deleteGenre(genre[0])">-</button></li>
                    </ul>
                </div>
                <div class="add_book_container">
                    <h3>Favourite Books</h3>
                    <div class="genre_div">
                        <p>Your Books:</p>
                        <button class="add_genre_btn" @click="openBookModal">Add Book</button>
                    </div>
                    <ul class="favourite_book_ul">
                        <li class="user_genre" style="background-color: grey;" v-if="user_data?.favourite_books?.length == 0">No books added yet</li>
                        <li class="favourite_book_li" v-for="book in user_data.favourite_books" :key="book">
                            <img :src="book?.image" class="favourite_book_image">
                            <div class="favourite_books_li_container">
                                <div class="favourite_books_li_div">
                                    <p class="favourite_book_div_title"><b>Title: </b>{{ book?.title }}</p>
                                    <p class="favourite_book_div_published"><b>Published: </b>{{ book?.published_date|| "Not specified" }}</p>
                                    <div class="favourite_books_li_authors">
                                        <p><b>Authors: </b></p>
                                        <li style="padding-right: 0.3rem;" v-for="(author,index) in book?.authors" :key="index">
                                            <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                        </li>
                                    </div>
                                    <div class="favourite_books_li_categories">
                                        <p style="padding-right: 0.5rem;"><b>Categories:</b></p>
                                        <ul v-if="book?.categories?.length > 0" class="favourite_category_ul">
                                            <li class="rcmnd_genre_modal" style="background-color: darkblue;" v-for="category in book?.categories" :key="category">{{ category }}</li>
                                        </ul>
                                        <ul v-else class="category_ul_modal">
                                            <li class="rcmnd_genre_modal" style="background-color: #9b9a9a;">Unknown</li>
                                        </ul>
                                    </div>
                                </div>
                                <button class="favourite_more_info" @click="moreInfo(book,true)">More info</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>  
            <div v-if="openAddGenre == true" class="genre_modal">
                <div class="genre_modal_container">
                    <h4>Add Genres</h4>
                    <div class="genre_modal_div">
                        <p>Choose from genres below</p>
                        <input type="text" v-model="newGenreName"  placeholder="Enter your own genre" maxlength="25"/>
                        <button @click="addNewGenre">Add</button>
                    </div>
                    <ul class="add_genre_list">
                        <li v-if="genreList.filter(genre => !user_data.favourite_genres.some(favGenre => favGenre[0] === genre[0])).length == 0" class="add_user_genre" style="background-color: grey;">No more genres available to add</li>
                        <li v-for="genre in genreList.filter(genre => !user_data.favourite_genres.some(favGenre => favGenre[0] === genre[0]))" :key="genre[0]" class="add_user_genre" :style=" {backgroundColor: genre[1] } ">{{ genre[0] }}<button @click="addGenre(genre[0])" class="add_existing_genre_btn">+</button></li>
                    </ul>
                    <button @click="cancelAddGenre" class="cancel_add_genre_btn">Exit</button>
                </div>
            </div>  
            <div v-if="openAddBook == true" class="genre_modal">
                <div class="book_modal_container">
                    <div class="book_modal_container_header">
                        <h4>Add Books</h4>
                        <input v-model="query" @input="searchBook(true)"  type="text" placeholder="Search Books - Trending Books"/>
                        <button @click="clearQuery" class="clear_book_btn">&times;</button>
                        <button v-if="showList == false" class="book_back_btn" @click="backToShowList">Back</button>
                        <button @click="exitAddBook" class="cancel_add_book_btn">Exit</button>
                    </div>
                    <ul class="books_ul_container" v-if="showList == true">
                        <div class="books_ul">
                            <div v-if="searchedBooks.length == 0 && isLoading == false" class="no_more_books_dashboard">
                                <p>No more book results</p>
                                <button @click="searchBook(true)">Go Back</button>
                            </div>
                            <li class="books_li_modal" v-for="book in searchedBooks" :key="book.id">
                                <img :src="book.volumeInfo?.imageLinks?.thumbnail" class="book_image_modal">
                                <div class="books_li_container_modal">
                                    <div class="books_li_div_modal">
                                        <p class="book_div_title_modal"><b>Title: </b>{{ book.volumeInfo?.title }}</p>
                                        <p class="book_div_published_modal"><b>Published: </b>{{ book.volumeInfo?.publishedDate || "Not specified" }}</p>
                                        <div class="books_li_authors_modal">
                                            <p><b>Authors: </b></p>
                                            <li style="padding-right: 0.3rem;" v-for="(author,index) in book.volumeInfo?.authors" :key="index">
                                                <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                            </li>
                                        </div>
                                        <div class="books_li_categories_modal">
                                            <p style="padding-right: 0.5rem;"><b>Categories:</b></p>
                                            <ul v-if="book.volumeInfo?.categories?.length > 0" class="category_ul_modal">
                                                <li class="rcmnd_genre_modal" style="background-color: darkblue;" v-for="category in book?.volumeInfo?.categories" :key="category">{{ category }}</li>
                                            </ul>
                                            <ul v-else class="category_ul_modal">
                                                <li class="rcmnd_genre_modal" style="background-color: #9b9a9a;">Unknown</li>
                                            </ul>
                                        </div>
                                    </div>
                                    <button class="more_info_modal" @click="moreInfo(book,false)">Select</button>
                                </div>
                            </li>
                        </div>
                        <ul class="pagination_control_modal" v-if="searchedBooks.length != 0">
                            <button class="pagination_control_button_next_prev" :disabled="this.currentPage == 1" @click="prevPage">&lt;</button>
                            <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page1 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page1 ? 'bold' : ''}" :disabled="page1 > totalPages" @click="changePage(page1)">{{page1}}</button>
                            <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page2 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page2 ? 'bold' : ''}" :disabled="page2 > totalPages" @click="changePage(page2)">{{page2}}</button>
                            <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page3 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page3 ? 'bold' : ''}" :disabled="page3 > totalPages" @click="changePage(page3)">{{page3}}</button>
                            <button class="pagination_control_button_page" :style="{backgroundColor: this.currentPage == page4 ? '#41ceaa' : '#FBFFFE', fontWeight: this.currentPage == page4 ? 'bold' : ''}" :disabled="page4 > totalPages" @click="changePage(page4)">{{page4}}</button>
                            <button class="pagination_control_button_next_prev" :disabled="this.currentPage >= totalPages" @click="nextPage">&gt;</button>
                        </ul>
                    </ul>
                    <div v-else-if="showList == false" class="chosen_book_div_modal">
                        <div class="chosen_book_container_modal">
                            <img :src="chosen_book?.image" class="chosen_book_image_modal">
                            <div class="chosen_book_div1_modal">
                                <div class="modal_title_div">
                                    <p class="modal_title1"><b>Title: </b>{{ chosen_book?.title || 'Title unavailable' }}</p>
                                    <button class="favourite_book_btn" v-if="isBookInFavourites(chosen_book) == true" @click="deleteFavouriteBook">Unfavourite</button>
                                    <button class="favourite_book_btn" v-else-if="isBookInFavourites(chosen_book) == false" @click="addFavouriteBook">Add to Favourites</button>
                                </div>
                                <ul class="chosen_book_authors_dashboard">
                                    <div class="chosen_book_authors_dashboard_div">
                                        <p><b>Authors: </b></p>
                                        <li v-for="(author,index) in chosen_book?.authors" :key="index">
                                            <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                        </li>
                                    </div>
                                    <div class="star_rating_div_dashboard">
                                        <p>Your rating: </p>
                                        <button
                                        v-for="star in stars"
                                        :key="star"
                                        @click="rateBook(star)"
                                        @mouseover="hoverStar(star)"
                                        @mouseleave="resetHover"
                                        :class="['star_dashboard',{hovered: hoveredStar >= star, filled: rating >= star}]"
                                        >
                                        <span v-html="hoveredStar >= star || rating >= star ? '&#9733;' : '&#9734;'"></span>
                                        </button>
                                    </div>
                                </ul>
                                <p><b>Published Date: </b>{{ chosen_book?.published_date }}</p>
                                <ul v-if="chosen_book?.categories?.length > 0" class="chosen_genre_list">
                                    <p><b>Categories: </b> </p>
                                    <li class="chosen_genre" style="background-color: grey;" v-for="category in chosen_book?.categories" :key="category">{{ category}}</li>
                                </ul>
                                <ul v-else class="chosen_genre_list">
                                    <p><b>Categories: </b> </p>
                                    <li class="chosen_genre" style="background-color: #9b9a9a;">Unknown</li>
                                </ul>
                                <p><b>Description: </b>{{ chosen_book?.description || 'Description unavailable' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>  
        </div>
    </div>
</template>
<script>
import { useUserStore } from '@/stores/userStore';
export default{
    name:"DashboardPage",
    data() {
        return{
            user_data: {
                favourite_genres : []
            },
            password_form: {},
            csrfToken: "",
            readUsername: true,
            readOnlineId: true,
            readDOB: true,
            changePassword: false,
            showOldPassword: false,
            showNewPassword1: false,
            showNewPassword2: false,
            openAddGenre: false,
            openAddBook: false,
            genreList: [],
            newGenreName: "",
            searchedBooks: [],
            query: '',
            currentPage: 1,
            totalPages: 1,
            showList: true,
            chosen_book: {},
            showPageMultiplier: 1,
            rating: 0,
            stars: [1,2,3,4,5],
            hoveredStar: 0,
            isLoading : false,
        }
    },
    computed: {
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
        userStore(){
            return useUserStore();
        }
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
        async fetch_user(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                     },
                    credentials: "include", 
                });


                if (response.ok){
                    const data = await response.json();
                    this.user_data = data;
                    this.user_data.favourite_genres = data.favourite_genres;
                    this.userStore.setUser(data.id, data.username, data.online_id, data.favourite_genres);
                    console.log("Fetched user data");
                }

            }
            catch (error){
                console.error(`${error}`)
            }
        },
        async searchBook(newSearch){
            this.showList = true;
            this.chosen_book = {};
            this.isLoading = true;

            if (newSearch == true){
                this.currentPage = 1;
                this.showPageMultiplier = 1;
            }
            try{
                const response = await fetch(`http://127.0.0.1:8000/search-book/?title=${this.query}&page=${this.currentPage}`);
                if (!response.ok){
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                this.searchedBooks = data.books || [];
                this.currentPage = data.current_page || 1;
                this.totalPages = data.total_pages || 1;
            }
            catch (error){
                console.error('error catching data', error)
            }
            this.isLoading = false;
            
        },
        async logout(){
            try{

                const response = await fetch("http://127.0.0.1:8000/logout/",
                {    
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                });
                if (!response.ok){
                    throw new Error('Failed to logout');
                }
                this.userStore.clearUser();
                window.location.href = "http://127.0.0.1:8000/login";

            }
            catch (error){
                console.error('error logging out', error)
            }

        },
        backToShowList(){
            this.showList = true;
            this.chosen_book = {};
        },
        exitAddBook(){
            this.openAddBook = false;
            this.clearQuery();
            this.chosen_book = {};
        },
        clearQuery(){
            this.query = '';
            this.searchBook(true);
        },
        changePage(pageNumber){
            this.currentPage = pageNumber;
            this.searchBook(false);
        },
        nextPage(){
            if (this.currentPage < this.totalPages){
                this.currentPage++;

                if (this.currentPage > this.page4){
                    this.showPageMultiplier++;
                }
                this.searchBook(false);

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
            this.searchBook(false);
        },
        openBookModal(){
            this.openAddBook = true;
            this.showList = true;
        },
        moreInfo(book_object, inFavourite){
            if (inFavourite == false){
                this.chosen_book.id = book_object.id;
                this.chosen_book.image = book_object.volumeInfo?.imageLinks?.thumbnail;
                this.chosen_book.title = book_object.volumeInfo?.title;
                this.chosen_book.authors = book_object.volumeInfo?.authors;
                this.chosen_book.published_date = book_object.volumeInfo['publishedDate']|| "Not specified";
                this.chosen_book.categories = book_object.volumeInfo?.categories;
                this.chosen_book.description = book_object.volumeInfo?.description;
            }
            else{
                this.chosen_book = book_object;
                this.openAddBook = true;
            }
            this.fetch_book_rating();
            this.showList = false;

        },
        async addFavouriteBook(){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ book: this.chosen_book, action: "add_book" }),
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
                this.fetch_user();
            }
            catch (error){
                console.error("Error adding book:", error);
            }
        },
        async deleteFavouriteBook(){
            try{
                const response = await fetch("http://127.0.0.1:8000/user/",
                {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ book: this.chosen_book, action: "delete_book" }),
                    credentials: "include", 
                })
                if (!response.ok) {
                    throw new Error(`Failed to remove book: ${response.status}`);
                }
                this.fetch_user();
            }
            catch (error){
                console.error("Error removing book:", error);
            }
            
        },
        isBookInFavourites(book){
            return this.user_data.favourite_books.some(favBook => favBook.title === book.title);
        },
        async saveUsername(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ username: this.user_data.username})
                });

                if (response.ok) {
                    console.log("Username updated successfully");
                    this.readUsername = true;
                    this.fetch_user();
                }
            }
            catch (error){
                console.error("Error updating username:", error)
            }
        },
        changeUsername(){
            this.readUsername = false;
            this.cancelOnlineId();
            this.cancelDOB();
        },
        cancelUsername(){
            this.fetch_user();
            this.readUsername = true;
        },
        async saveOnlineId(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ online_id: this.user_data.online_id})
                });

                if (response.ok) {
                    console.log("Online ID updated successfully");
                    this.readOnlineId = true;
                    this.fetch_user();
                }
            }
            catch (error){
                console.error("Error updating online ID:", error)
            }
        },
        changeOnlineId(){
            this.readOnlineId = false;
            this.cancelUsername();
            this.cancelDOB();
        },
        cancelOnlineId(){
            this.fetch_user();
            this.readOnlineId = true;
        },
        async saveDOB(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ DOB: this.user_data.DOB})
                });

                if (response.ok) {
                    console.log("DOB updated successfully");
                    this.readDOB = true;
                    this.fetch_user();
                }
            }
            catch (error){
                console.error("Error updating DOB:", error)
            }
        },
        changeDOB(){
            this.readDOB = false;
            this.cancelUsername();
            this.cancelOnlineId();
        },
        cancelDOB(){
            this.fetch_user();
            this.readDOB = true;
        },
        change_password(){
            this.cancelUsername();
            this.cancelOnlineId();
            this.cancelDOB();
            this.changePassword = true;
        },
        cancelPassword(){
            this.password_form.old_password = "";
            this.password_form.new_password_1 = "";
            this.password_form.new_password_2 = "";
            this.changePassword = false;
        },
        async updatePassword(){
            try{
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({
                        action : 'change_password',
                        old_password : this.password_form.old_password,
                        new_password1 : this.password_form.new_password_1,
                        new_password2 : this.password_form.new_password_2
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    let errorMessage = Object.values(data.errors || {}).flat().join("\n");
                    throw new Error(errorMessage || "Unexpected error occured when changing password");
                }
                this.cancelPassword();
            }
            catch (error) {
                console.error("Error:", error);
                alert(error);
            }

        },
        show_OldPassword(){
            this.showOldPassword = !this.showOldPassword;
        },
        show_NewPassword1(){
            this.showNewPassword1 = !this.showNewPassword1;
        },
        show_NewPassword2(){
            this.showNewPassword2 = !this.showNewPassword2;
        },
        clearOldPassword(){
            this.password_form.old_password = '';
        },
        clearNewPassword1(){
            this.password_form.new_password_1 = '';
        },
        clearNewPassword2(){
            this.password_form.new_password_2 = '';
        },
        openGenreModal(){
            this.openAddGenre = true;
        },
        async deleteGenre(genreName){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ genre_name: genreName , action: "delete_genre" }),
                    credentials: "include", 
                })
                if (!response.ok) {
                    throw new Error(`Failed to remove genre: ${response.status}`);
                }
                this.fetch_user();
            }
            catch (error){
                console.error("Error removing genre:", error);
            }
        },
        async addGenre(genreName){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ genre_name: genreName , action: "add_genre" }),
                    credentials: "include", 
                })
                if (!response.ok) {
                    throw new Error(`Failed to add genre: ${response.status}`);
                }
                this.fetch_user();
            }
            catch (error){
                console.error("Error adding genre:", error);
            }
        },
        async addNewGenre(){

            if (!this.newGenreName || this.newGenreName.trim().length == 0){
                alert("Please provide a new genre name");
                return;
            }

            try{
                const response = await fetch("http://127.0.0.1:8000/genre/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ genre_name: this.newGenreName}),
                    credentials: "include", 
                })
                if (!response.ok) {
                    throw new Error(`Failed to add new genre: ${response.status}`);

                }

                let data = await response.json();
                let new_genre = data.genre_name;
                this.addGenre(new_genre);

                this.newGenreName = "";
                this.fetch_user();
                this.fetch_genres();
            }
            catch (error){
                console.error("Error adding new genre:", error);
                alert("Error:" + error.message);
            }

        },
        async fetch_genres(){
            try{
                const response = await fetch("http://127.0.0.1:8000/genre/",
                {    
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                });
                if (!response.ok) {
                    throw new Error(`Failed to fetch genres: ${response.status}`);
                }
                this.genreList = await response.json();
            }
            catch (error){
                console.error("Error fetching genres:", error);
            }
        },
        cancelAddGenre(){
            this.openAddGenre = false;
        },
        async fetch_book_rating(){
            try
            {
                const response = await fetch(`http://127.0.0.1:8000/book-rating/?book_id=${this.chosen_book.id}`,
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
        },
        async rateBook(rating){

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
                    body: JSON.stringify({ book_id: this.chosen_book.id, book_rating: rating }),
                    credentials: "include", 
                })
                if (!response.ok) {
                        throw new Error(`Failed to add book: ${response.status}`);
                    }
            }
            catch (error){
                console.error("Error adding book:", error);
            }
        },
        hoverStar(star){
            this.hoveredStar= star;
        },
        resetHover(){
            this.hoveredStar = 0;
        },

    },
    async mounted() {
        await this.fetch_csrf_token();
        this.fetch_user();
        this.fetch_genres();
        this.searchBook();
    }
};
</script>
<style>

body{
    background-color: rgba(247, 244, 244, 0.944);
}

.page_container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.dashboard_container{
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
    width: 80rem;
    height: 35rem;
}
.no_more_books_dashboard{
    margin-top: 2rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 26rem;
    justify-content: space-between;
}
.no_more_books_dashboard p{
    border-radius: 0.8rem;
    background: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 1.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.7rem;
    padding-bottom: 0.7rem;
}
.no_more_books_dashboard button{
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
.no_more_books_dashboard button:hover{
    background-color: #e51635c5;

}

.user_info{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    background-color: #FBFFFE; 
    width: 31rem;   
    height: 27rem;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
}
.user_info_header{
    font-size: 1.8rem;
    margin: 0;
    align-self: center;
    margin-bottom: 1.5rem;
}
.user_info_list{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 31rem;
    height: 24rem;
    margin: 0;
    padding: 0;
    margin-left: 1rem;
    gap: 1rem;

}
.user_info_li p{
    margin: 0;
    padding: 0;
}
.user_info_li{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.user_info_li b{
    font-size: 1.2rem;
}
.user_info_div{
    margin-top: 0.5rem;
    display: flex;
    flex-direction: row;
    width: 28.7rem;
    justify-content: space-between;
}
.user_info_div_input {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    font-size: 1.2rem;
    border: 3px solid #1B1B1E;
    padding-left: 0.5rem;
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    width: 17.5rem;
    border-radius: 0.5rem;
}
.user_info_div_date{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    font-size: 1.2rem;
    border: 3px solid #1B1B1E;
    padding-left: 0.5rem;
    padding-top: 0.47rem;
    padding-bottom: 0.47rem;
    width: 17.5rem;
    border-radius: 0.5rem;

}

.user_genres{
    background-color: aliceblue;  
    width: 35rem;
}

.change_btn{
    all: unset;
    background-color: #0dc43b;
    font-size: 1.2rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.change_btn:hover{
    background-color: #0dc43bae;
}

.button_div{
    margin-top: 2rem;
}

.save_btn{
    all: unset;
    background-color: #0fb485;
    font-size: 1.1rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.save_btn:hover{
    background-color: rgba(13, 196, 144, 0.823);
}
.cancel_btn{
    all: unset;
    background-color: #e51635;
    font-size: 1.1rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.cancel_btn:hover{
    background-color: #ff1538be;
}

.change_div{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 9.5rem;
}
.change_password_btn{
    all: unset;
    margin-top: 1rem;
    height: 3rem;
    width: 10rem;
    font-size: 1.2rem;
    font-weight: 401;
    align-self: flex-start;
    color: #FBFFFE;
    background-color: #c7142f;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}

.change_password_btn:hover{
    background-color: #c7142fa8;

}

.password_btn_div{
    width: 20.4rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.update_btn{
    all: unset;

    height: 3rem;
    width: 10rem;
    font-size: 1.2rem;
    font-weight: 401;
    align-self: flex-start;
    color: #FBFFFE;
    background-color: #0fb485;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.update_btn:hover{
    background-color: rgba(13, 196, 144, 0.823);
}
.cancel_password_btn{
    all: unset;
    height: 3rem;
    background-color: #e51635;
    font-size: 1.2rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.cancel_password_btn:hover{
    background-color: #ff1538be;
}
.user_password_div{
    margin-top: 0.5rem;
    display: flex;
    flex-direction: row;
    width: 31rem;

}
.show_password_btn{
    all: unset;
    background-color: #FAA916;
    color: #FBFFFE;
    width: 3rem;
    font-weight: 401;
    font-size: 1.1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    margin-left: 0.3rem;
    transition: 0.2s ease;
}
.show_password_btn:hover{
    background-color: #faaa16b4;
}
.clear_password_btn{
    all: unset;
    background-color: #e51635;
    color: #FBFFFE;
    font-weight: 401;
    font-size: 1.1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    margin-left: 0.3rem;
    transition: 0.2s ease;

}
.clear_password_btn:hover{
    background-color: #e51635b9;
}
.add_book_container{
    margin-top: 1rem;
    width: 41.5rem;
    height: 22rem;
    background-color: #FBFFFE;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 2rem;
}
.add_book_container h3{
    margin: 0;
    margin-top: 1rem;
    margin-bottom: 0.6rem;
    align-self: center;
    margin-right: 2rem;

}
.book_modal_container{
    display: flex;
    flex-direction: column;
    background-color: #FBFFFE;
    width: 80rem;
    height: 40rem;
    max-height: 40rem;
    padding-left: 2rem;
    padding-right: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.chosen_book_authors_dashboard{
    padding: 0;
    display: flex;
    flex-direction: row;
    width: 55rem;
    justify-content: space-between;
    align-items: center;
}
.chosen_book_authors_dashboard_div{
    padding: 0;
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    width: 40rem;
    max-width: 40rem;
    flex-wrap: wrap;
}
.genre_book_container{
    width: 43.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.books_li_modal{
    display: flex;
    flex-direction: row;
    min-width: 16rem;
    width: 16rem;
    max-width: 16rem;
    max-height: 12rem;
    font-size: 0.85rem;
    padding: 1rem;
    gap: 0.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

.books_li_modal:hover{
    transform: scale(1.06);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.books_li_div_modal{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    height: 10.5rem;

}
.books_li_modal p{
    gap: 0;
    margin: 0;
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.books_ul_container{
    display: flex;
    flex-direction: column;
    height: 40rem;
    max-height: 40rem;
    overflow-y: auto;
    overflow-x: hidden;
    align-items: center;
}
.books_ul{
    background-color: #FBFFFE;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 77rem;
    justify-content: flex-start;
    gap: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.books_ul::-webkit-scrollbar{
    width: 7px;
}

.books_ul::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_ul::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_container_modal{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 12rem;
}
.book_div_title_modal{
    max-height: 4rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    width: 8rem;
    max-width: 8rem;
    font-size: 0.8rem;
    padding-right: 0.1rem;
}
.book_div_title_modal::-webkit-scrollbar{
    width: 3px;
}

.book_div_title_modal::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.book_div_title_modal::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.book_div_published_modal{
    width: 8rem;
    max-width: 8rem;
    font-size: 0.75rem;
}
.more_info_modal{
    align-self: center;
    justify-self: flex-end;
    width: 7rem;
    height: 1.3rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.75rem;
    transition: 0.2s ease;
}

.more_info_modal:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.category_ul_modal{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    margin: 0;
    padding: 0;
}
.rcmnd_genre_modal{
    display: inline-block;
    color: #FBFFFE;
    padding-right: 0.3rem;
    padding-left: 0.3rem;
    padding-top: 0.15rem;
    padding-bottom: 0.15rem;
    border-radius: 0.3rem;
    max-width: 7rem;
    font-size: 0.75rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.book_image_modal{
    min-height: 12rem;
    max-height: 12rem;
    height: 12rem;
    min-width: 8rem;
    width: 8rem;
    max-width: 8rem;
    border-radius: 0.3rem;
}
.books_li_categories_modal{
    width: 8rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    max-height: 10rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    padding-right: 0.1rem;
    font-size: 0.8rem;
}
.books_li_categories_modal::-webkit-scrollbar{
    width: 3px;
}

.books_li_categories_modal::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_categories_modal::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_modal p {
    gap: 0;
    margin: 0;
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.books_li_authors_modal{
    width: 8rem;
    max-height: 2.3rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    font-size: 0.8rem;
    padding-right: 0.1rem
}
.books_li_authors_modal p{
    padding-right: 0.3rem;
    font-size: 0.8rem;
}
.books_li_authors_modal::-webkit-scrollbar{
    width: 3px;
}

.books_li_authors_modal::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_authors_modal::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}

.add_genre_container{
    width: 41.5rem;
    height: 13rem;
    background-color: #FBFFFE;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 2rem;
}
.add_genre_container h3{
    margin-bottom: 0.7rem;
    align-self: center;
    margin-right: 2rem;

}

.add_genre_btn{
    all: unset;
    font-size: 1.1rem;
    height: 2.5rem;
    font-weight: 401;
    color: #1B1B1E;
    background-color: #FAA916;
    border-radius: 0.5rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    transition: 0.2s ease;
}
.add_genre_btn:hover{
    background-color: #faaa16b9;
    color: #1b1b1ea8;
}
.genre_div{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 39.5rem;
    justify-content: space-between;
}
.genre_div p {
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    font-size: 1.1rem;
    height: 2.5rem;
    font-weight: 401;
    color: #1B1B1E;
    background-color: #41ceaa;
    border-radius: 0.5rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
}
.genre_modal{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    background: rgba(0,0,0,0.5);
    width: 100%;
    height: 100%;
}
.genre_modal_container{
    display: flex;
    flex-direction: column;
    background-color: #FBFFFE;
    width: 36rem;
    max-height: 29rem;
    padding-left: 2rem;
    padding-right: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.genre_modal_container h4{
    font-size: 1.5rem;
    margin: 0;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}
.user_genre_list{
    padding-left: 0;
    padding-top: 0.3rem;
    width: 39.5rem;
    max-width: 39.5rem;
    height: 5rem;
    max-height: 5rem;
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    overflow-x: hidden;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding-right: 1rem;
}
.user_genre_list::-webkit-scrollbar{
    width: 5px;
}

.user_genre_list::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.user_genre_list::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.user_genre{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    color: #FBFFFE;
    font-size: 1rem;
    height: 2rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.3rem;
}
.delete_genre_btn{
    padding: 0;
    margin: 0;
    all: unset;
    position: absolute;
    top: -4px;
    right: -4px;
    background-color: #c7142f;
    height: 0.9rem;
    width: 0.9rem;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.9rem;
    font-size: 1.2rem;
    text-align: right;
    font-weight: 501;
}
.delete_genre_btn:hover{
    background-color: #c7142fba;
}
.add_genre_list{
    padding: 0;
    margin: 0;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    width: 37rem;
    max-width: 37rem;
    max-height: 15rem;
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    overflow-x: hidden;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 0.7rem;
}
.add_genre_list::-webkit-scrollbar{
    width: 5px;
}

.add_genre_list::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.add_genre_list::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.add_user_genre{
    position: relative;
    margin: 0;
    padding: 0;
    height: 2.1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    color: #FBFFFE;
    border-radius: 0.3rem;

}
.add_existing_genre_btn{
    padding: 0;
    margin: 0;
    all: unset;
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #06b930;
    height: 0.9rem;
    width: 0.9rem;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.9rem;
    font-size: 0.9rem;
    text-align: right;
    font-weight: 401;
    transition: 0.2s ease;
}
.add_existing_genre_btn:hover{
    background-color: #19d745;
}
.genre_modal_div{
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 3rem;
    padding-bottom: 1rem;
    width: 37rem;
}
.genre_modal_div p{
    margin: 0;
    padding: 0;
    background-color: #41ceaa;
    color: #1B1B1E;
    font-weight: 401;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    padding: 0.5rem;
    border-radius: 0.5rem;
}
.genre_modal_div input{
    all: unset;
    margin-left: 5.5rem;
    padding-left: 0.5rem;
    text-align: left;
    border: 3px solid #1B1B1E;
    height: 2rem;
    width: 12rem;
    border-radius: 0.4rem;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.genre_modal_div button{
    all: unset;
    margin-left: 0.5rem;
    height: 2.3rem;
    background-color: #FAA916;
    font-weight: 401;
    color: #1B1B1E;
    width: 4rem;
    font-size: 1.1rem;
    border-radius: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.2s ease;
}
.genre_modal_div button:hover{
    background-color: #faaa16c3;
    color: #1b1b1eac;
}
.cancel_add_genre_btn{
    all: unset;
    align-self: flex-end;
    margin-top: 0.7rem;
    margin-bottom: 1.2rem;
    width: 5rem;
    height: 2.5rem;
    background-color: #e61534;
    color: #FBFFFE;
    font-weight: 401;
    border-radius: 0.4rem;
    transition: 0.2s ease;
}
.cancel_add_genre_btn:hover{
    background-color: #e61534c8;
}

.chosen_book_div_modal{
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    align-self: center;
    width: 80rem;
    max-height: 32rem;
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.chosen_book_div_modal::-webkit-scrollbar{
    width: 7px;
}

.chosen_book_div_modal::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.chosen_book_div_modal::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.chosen_book_container_modal{
    display: flex;
    flex-direction: row;
    width: 70rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    border-radius: 1rem;
    padding: 2rem;
    margin-top: 0.7rem;
    margin-bottom: 0.5rem;
}
.chosen_book_image_modal{
    height: 25.2rem;
    max-height: 25.2rem;
    width: 18rem;
    max-width: 15rem;
    border-radius: 0.8rem;
}
.chosen_book_div1_modal{
    display: flex;
    width: 54rem;
    max-width: 54rem;
    flex-direction: column;
    align-items: flex-start;
    margin-left: 1rem;
    min-height: 10rem;
}
.modal_title1{
    width: 43rem;
    max-width: 43rem;
}
.modal_title_div{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}
.chosen_book_div1_modal p{
    gap: 0%;
    padding: 0%;
    margin: 0%;
    text-align: left;
}
.book_modal_container_header{
    margin-top: 2rem;
    margin-left: 2.5rem;
    align-self: flex-start;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    height: 2.5rem;
    width: 77.5rem;

}
.book_modal_container_header h4{
    margin: 0;
    padding: 0;
    font-size: 1.9rem;
}
.book_modal_container_header input{
    width: 23rem;
    height: 2.4rem;
    border-radius: 1rem;
    font-size: 1.2rem;
    border: 3px solid #1B1B1E;
    border-radius: 0;
    border-top-left-radius: 0.6rem;
    border-bottom-left-radius: 0.6rem;
    border-right: none;
    padding-left: 0.5rem;
    outline: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    justify-self: center;
    margin-left: 14rem;
}
.clear_book_btn{
    all: unset;
    height: 2.9rem;
    background-color: #e91938;
    width: 2.8rem;
    border-radius: 0;
    border-top-right-radius: 0.6rem;
    border-bottom-right-radius: 0.6rem;
    font-weight: 401;
    color: #FBFFFE;
    font-size: 1.8rem;
    transition: 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.clear_book_btn:hover{
    background-color: #e91938d4;
    font-weight: 501;
}
.cancel_add_book_btn{
    all: unset;
    margin-left: auto;
    width: 5rem;
    font-size: 1.2rem;
    height: 2.9rem;
    background-color: #e61534;
    color: #FBFFFE;
    font-weight: 401;
    border-radius: 0.6rem;
    transition: 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.cancel_add_book_btn:hover{
    background-color: #e61534c8;
}

.favourite_book_btn{
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
.favourite_book_btn:hover{
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.book_back_btn{
    all: unset;
    margin-left: 16.5rem;
    height: 2.5rem;
    border: solid 3px #FAA916;
    transition: 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    color: #FAA916;
    font-weight: 401;
    border-radius: 0.6rem;
    font-size: 1.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
.book_back_btn:hover{
    background-color: #FAA916;
    color: #FBFFFE;
}
.pagination_control_modal{
    padding: 0;
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
}
.favourite_book_ul{
    padding: 0;
    width: 40.3rem;
    max-width: 40.3rem;
    height: 15rem;
    max-height: 15rem;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 1rem;
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    padding-left: 0.2rem;
    padding-bottom: 1rem;
    padding-top: 0.5rem;
}
.favourite_book_ul::-webkit-scrollbar{
    width: 5px;
}

.favourite_book_ul::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.favourite_book_ul::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.favourite_book_li{
    padding: 1rem;
    display: flex;
    flex-direction: row;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    width: 17rem;
    max-width: 17rem;
    height: 11.2rem;
    max-height: 11.2rem;
    border-radius: 1rem;
    gap: 0.5rem;
    transition: 0.3s ease;
}
.favourite_book_li:hover{
    transform: scale(1.03);
}
.favourite_book_image{
    min-height: 11.1rem;
    max-height: 11.1rem;
    height: 11.1rem;
    min-width: 7.2rem;
    width: 7.2rem;
    max-width: 7.2rem;
    border-radius: 0.3rem;
}
.favourite_books_li_container{
    display: flex;
    flex-direction: column;
    height: 12rem;
    width: 100%;
}
.favourite_books_li_div{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    height: 10rem;
}
.favourite_books_li_div p{
    gap: 0;
    margin: 0;
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.favourite_book_div_title{
    padding: 0;
    margin: 0;
    width: 10rem;
    max-width: 10rem;
    font-size: 0.8rem;
    max-height: 4rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.favourite_book_div_title::-webkit-scrollbar{
    width: 3px;
}
.favourite_book_div_title::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.favourite_book_div_title::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.favourite_book_div_published{
    width: 9.6rem;
    max-width: 9.6rem;
    font-size: 0.8rem;
}
.favourite_books_li_authors{
    width: 9.5rem;
    max-width: 9.5rem;
    max-height: 3rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    font-size: 0.8rem;
    padding-right: 0.5rem;
}
.favourite_books_li_authors p{
    padding-right: 0.3rem;
    font-size: 0.8rem;
}
.favourite_books_li_authors::-webkit-scrollbar{
    width: 3px;
}

.favourite_books_li_authors::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.favourite_books_li_authors::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.favourite_books_li_categories{
    width: 10rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    max-height: 5rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    font-size: 0.8rem;
}
.favourite_books_li_categories::-webkit-scrollbar{
    width: 3px;
}

.favourite_books_li_categories::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.favourite_books_li_categories::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.favourite_category_ul{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 0.5rem;
    margin: 0;
    padding: 0;
}
.favourite_more_info{
    align-self: center;
    width: 7rem;
    height: 1.3rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.75rem;
    transition: 0.2s ease;
}

.favourite_more_info:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.star_rating_div_dashboard{
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 14rem;
}
.star_rating_div_dashboard p{
    font-size: 1rem;
    margin-right: 0.5rem;
    font-weight: 501;
}
.star_dashboard{
    all: unset;
    background: none;
    border: none;
    font-size: 1.5rem;
    font-weight: 601;
    cursor: pointer;
    color: #FAA916;
}
.star_dashboard:hover{
    color: #FAA916;
}
.star_dashboard.filled{
    color: #FAA916;
}
</style>