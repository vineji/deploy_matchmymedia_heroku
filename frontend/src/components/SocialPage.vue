<template>
    <div class="social_container">
        <div class="user_list_container">
            <h1>Other Users</h1>
            <div class="sort_filter_container">
                <div class="sort_by_container">
                    <button class="sort_button" @click="fetch_all_user">Sort by</button>
                    <select class="sort_select" v-model="sortBy">
                        <option value="Most Common" >Most Common Genres</option>
                        <option value="Least Common" >Least Common Genres </option>
                    </select>
                </div>
                <div class="filter_by_container">
                    <button class="filter_button" @click="fetch_all_user">Filter</button>
                    <label>Min age:</label>
                    <input type="number" min="10" max="100" v-model.number="minAge">
                    <label>Max age:</label>
                    <input type="number" v-model.number="maxAge" min="10" max="100">
                    <button class="reset_button" @click="reset">Reset</button>
                </div>
            </div>
            <li class="user_box_not_found" v-if="userList.length == 0"> No users found</li>
            <li v-for="user in userList" :key="user" class="user_box">
                <div class="user_box_header">
                    <p><b>Online ID: </b>{{user.online_id}}</p>
                    <button class="add_friend_btn" v-if="user.is_friend == true">Friend</button>
                    <button class="add_friend_btn" v-if="user.is_friend == false" @click="sendFriendRequest(user.id)">Add Friend</button>
                </div>
                <p><b>Favourite genres:</b></p>
                <ul class="user_list_genre_container">
                    <li v-if="user.favourite_genres.length == 0"  class="user_list_genre" >No genres added yet</li>
                    <li v-for="genre in user.favourite_genres" :key="genre" :style="{backgroundColor: genre[1]}"  class="user_list_genre" >{{genre[0]}}</li>
                </ul>
                <button class="view_more_btn" @click="viewMore(user)">View More</button>
                <div v-if="user.showMore == true" class="other_user_modal">
                    <div class="other_user_modal_container">
                        <div class="other_user_modal_header">
                            <h1 v-if="showMoreInfo == false">User Profile</h1>
                            <h1 v-if="showMoreInfo == true">Book Information</h1>
                            <div class="header_button_div">
                                <button v-if="showMoreInfo == true" @click="backPage" class="back_btn">Back</button>
                                <button @click="closeViewMore(user)" class="close_btn">Close</button>
                            </div>
                        </div>
                        <div class="other_user_info_div" v-if="showMoreInfo == false">
                            <p><b>Online ID: </b>{{user.online_id}}</p>
                            <p><b>Favourite Genres:</b></p>
                            <ul class="other_user_genre_container">
                                <li v-if="user.favourite_genres.length == 0"  class="other_user_genre" >No genres added yet</li>
                                <li v-for="genre in user.favourite_genres" :key="genre" :style="{backgroundColor: genre[1]}"  class="other_user_genre" >{{genre[0]}}</li>
                            </ul>
                            <p><b>Favourite Books:</b></p>
                            <ul class="other_user_book_container">
                                <li v-if="user.favourite_books.length == 0"> User has not favourited any books yet</li>
                                <li v-for="book in user.favourite_books" :key="book" class="other_user_book_li">
                                    <img :src="book.image" class="other_user_book_img"/>
                                    <div class="other_user_book_info_div">
                                        <p class="other_user_book_info_title"><b>Title: </b>{{ book.title || "Unavailable" }}</p>
                                        <p><b>Published: </b>{{ book.published_date || "Unavailable" }}</p>
                                        <ul class="other_user_book_info_authors" >
                                            <p style="padding-right: 0.5rem;"><b>Authors: </b></p>
                                            <li v-if="!book.authors || book.authors.length === 0">Unavailable</li>
                                            <li style="text-align: left;" v-for="(author,index) in book?.authors" :key="index">
                                                <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                            </li>
                                        </ul>
                                        <ul class="other_user_book_info_genres">
                                            <p style="padding-right: 0.5rem;"><b>Genres: </b></p>
                                            <li v-if="!book.categories || book.categories.length === 0" style="background-color: grey;" class="other_book_genre">Unavailable</li>
                                            <li v-for="category in book.categories" :key="category" class="other_book_genre">{{ category }}</li>
                                        </ul>
                                        <button @click="moreInfo(book)" class="other_book_more_info_btn" >More Info</button>
                                    </div>
                                </li>
                            </ul>
                        </div>
                        <div v-if="showMoreInfo == true" class="more_info_book_div" >
                            <img :src="moreInfoBook.image" class="more_info_book_img">
                            <div class="more_info_info_div">
                                <p><b>Title: </b>{{ moreInfoBook.title || "Unavailable" }}</p>
                                <p><b>Published: </b>{{ moreInfoBook.published_date || "Unavailable" }}</p>
                                <ul class="more_info_info_authors" >
                                    <p style="padding-right: 0.5rem;"><b>Authors: </b></p>
                                    <li v-if="!moreInfoBook.authors || moreInfoBook.authors.length === 0">Unavailable</li>
                                    <li style="text-align: left;" v-for="(author,index) in moreInfoBook?.authors" :key="index">
                                        <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                    </li>
                                </ul>
                                <ul class="more_info_info_genres_container">
                                    <p style="padding-right: 0.5rem;"><b>Genres: </b></p>
                                    <li v-if="!moreInfoBook.categories || moreInfoBook.categories.length === 0" style="background-color: grey;" class="more_info_info_genre">Unavailable</li>
                                    <li v-for="category in moreInfoBook.categories" :key="category" class="more_info_info_genre">{{ category }}</li>
                                </ul>
                                <p style="margin-top: 0.5rem;"><b>Description: </b>{{ moreInfoBook.description || "Unavailable" }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
            <div class="pagination_container">
                <button :disabled="hasPrevious == false" @click="prevPage()" class="pagination_button">Previous</button>
                <button :disabled="hasNext == false" @click="nextPage()" class="pagination_button">Next</button>
            </div>
        </div>
        <div class="other_container">
            <nav class="social_page_nav">
                <router-link class="nav_btn_dashboard" :to="{name: 'Dashboard Page'}">Dashboard</router-link>
                <router-link class="nav_btn_search_books" :to="{name: 'Main Page'}">Search Books</router-link>
            </nav>
            <div class="friend_request_container">
                <h2>Your Inbox</h2>
                <div class="friend_request_btn_container">
                    <div class="friend_request_type_btns">
                        <button class="friend_request_type_button1" :disabled="showRequestType === 'incoming request'" :class="{active: showRequestType === 'incoming request'}" @click="showRequestType = 'incoming request'">Incoming</button>
                        <button class="friend_request_type_button2" :disabled="showRequestType === 'outgoing request'" :class="{active: showRequestType === 'outgoing request'}" @click="showRequestType = 'outgoing request'">Outgoing</button>
                    </div>
                    <div class="friend_request_status_btns">
                        <button class="friend_request_status_button1" :disabled="showRequestStatus === 'pending'" :class="{active: showRequestStatus === 'pending'}" @click="showRequestStatus = 'pending'">Pending</button>
                        <button class="friend_request_status_button2" :disabled="showRequestStatus === 'declined'" :class="{active: showRequestStatus === 'declined'}"  @click="showRequestStatus = 'declined'">Declined</button>
                    </div>
                </div>
                <ul class="friend_request_ul" v-if="showRequestType === 'incoming request' && showRequestStatus === 'pending'">
                    <li class="friend_request_li" v-for="request in friendRequestList.filter(r => r.type == showRequestType && r.status == showRequestStatus)" :key="request">
                        <p v-if="request.type == 'incoming request'"><b>From: </b>{{ request.from_user_online_id }}</p>
                        <p><b>Status: </b>{{ request.status }}</p>
                        <div class="request_action_btns" v-if="request.type == 'incoming request' && request.status == 'pending'">
                            <button @click="acceptRequest(request.id)" class="accept_btn" > Accept</button>
                            <button @click="declineRequest(request.id)" class="decline_btn" > Decline</button>
                        </div>
                    </li>
                    <li v-if="friendRequestList.filter(r => r.type == showRequestType && r.status == showRequestStatus).length == 0" class="no_request_li">
                        No Requests
                    </li>
                </ul>
                <ul class="friend_request_ul1" v-if="!(showRequestType == 'incoming request' && showRequestStatus == 'pending')">
                    <li class="friend_request_li1" v-for="request in friendRequestList.filter(r => r.type == showRequestType && r.status == showRequestStatus)" :key="request">
                        <p v-if="request.type == 'incoming request'"><b>From: </b>{{ request.from_user_online_id }}</p>
                        <p v-if="request.type == 'outgoing request'"><b>To: </b>{{ request.to_user_online_id }}</p>
                        <p><b>Status: </b>{{ request.status }}</p>
                    </li>
                    <li v-if="friendRequestList.filter(r => r.type == showRequestType && r.status == showRequestStatus).length == 0" class="no_request_li">
                        No Requests
                    </li>

                </ul>
            </div>
        </div>
    </div>

</template>
<script>
import { useUserStore } from '@/stores/userStore';
export default {
    data() {
        return {
            userList : [],
            csrfToken : "",
            sortBy : "Most Common",
            minAge : null,
            maxAge : null,
            currentPage: 1,
            totalPages: 1,
            hasNext: false,
            hasPrevious: false,
            friendRequestList: [],
            friendshipList: [],
            showMoreInfo: false,
            moreInfoBook: {},
            showRequestType: "incoming request",
            showRequestStatus: "pending",
        }
    },
    setup(){
        const userStore = useUserStore();
        userStore.loadUser();
        return {userStore};
    },
    computed: {
        loggedUser(){
            return{
                id: this.userStore.user_id || null,
                online_id: this.userStore.online_id || null,
                favourite_genres: this.userStore.favourite_genres || [],
            }
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
        async fetch_all_user(page = 1){
            try{
                const params = new URLSearchParams();
                params.append('sort', this.sortBy.toString());
                params.append('page', page.toString())

                if (this.minAge !== null){
                    params.append('minAge', this.minAge);
                }
                if (this.maxAge !== null){
                    params.append('maxAge', this.maxAge);
                }

                const response = await fetch(`http://127.0.0.1:8000/user-list/?${params.toString()}`,
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.userList = data.user_list.map(user => ({
                        ...user,
                        showMore : false,
                    }));
                    this.currentPage = data.current_page;
                    this.totalPages = data.total_pages;
                    this.hasNext = data.has_next;
                    this.hasPrevious = data.has_previous;
                }
                else{
                console.log(`Failed to fetch user list, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching user list, ${error}`)
            }
        },
        async sendFriendRequest(friend_id){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/friend-request/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ friend_id : friend_id }),
                    credentials: "include", 
                })

                const data = await response.json();
                this.fetch_friend_requests();
                alert(data.message);
            }
            catch (error){
                console.error("Error sending request:", error);
            }
        },
        async fetch_friend_requests(){
            try{
                const response = await fetch(`http://127.0.0.1:8000/friend-request/`,
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.friendRequestList = data;
                }
                else{
                console.log(`Failed to fetch friend requests, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching friend requests, ${error}`)
            }
        },
        async acceptRequest(request_id){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/friend-request/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ request_id : request_id, action : "accept" }),
                    credentials: "include", 
                })
                this.fetch_friend_requests();
                this.fetch_all_user();
                const data = await response.json();

                alert(data.message);
            }
            catch (error){
                console.error("Error sending request:", error);
            }
        },
        async declineRequest(request_id){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/friend-request/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ request_id : request_id, action : "decline" }),
                    credentials: "include", 
                })
                this.fetch_friend_requests();
                this.fetch_all_user();
                const data = await response.json();

                alert(data.message);
            }
            catch (error){
                console.error("Error sending request:", error);
            }
        },
        viewMore(user){
            if (user.is_friend == false){
                alert("You needs to be friends to view more info");
            }
            else{
                user.showMore = !user.showMore;
            }
        },
        reset(){
            this.minAge = null;
            this.maxAge = null;
            this.sortBy = "Most Common";
            this.fetch_all_user();
        },
        moreInfo(book){
            this.showMoreInfo = true;
            this.moreInfoBook = book;
        },
        backPage(){
            this.showMoreInfo = false;
            this.moreInfoBook = null;
        },
        closeViewMore(user){
            user.showMore = false;
            this.showMoreInfo = false;
            this.moreInfoBook = null;
        },
        prevPage(){
            this.fetch_all_user(this.currentPage - 1);
            window.scrollTo({top: 0, behavior: 'smooth'});
        },
        nextPage(){
            this.fetch_all_user(this.currentPage + 1);
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

    },
    mounted(){
        this.fetch_csrf_token();
        this.fetch_all_user();
        this.fetch_friend_requests();
    }
}

</script>
<style>
.social_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;

}
.other_container{
    width: 50rem;
}
.user_list_container{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 60rem;

}
.user_box_not_found{
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 1.3rem;
    width: 39rem;
    padding-top: 1.5rem;
    padding-right: 1.5rem;
    padding-left: 1.5rem;
    padding-bottom: 1.5rem;
    background-color: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 2rem;
    gap: 1rem;
}
.user_box{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    border-radius: 1.3rem;
    width: 39rem;
    padding-top: 1.5rem;
    padding-right: 1.5rem;
    padding-left: 1.5rem;
    padding-bottom: 0.5rem;
    background-color: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 1.2rem;
    gap: 1rem;
}
.user_box p{
    padding: 0;
    margin: 0;
}
.user_box_header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}
.user_box_header p{
    margin: 0;
    padding: 0;
    text-align: left;
    font-size: 1.2rem;
    width: 28rem;
}
.user_box_header b{
    padding-right: 1rem;
}
.user_list_genre_container{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    max-height: 5rem;
    gap: 0.8rem;
    width: 100%;
    padding-left: 0.1rem;
    padding-bottom: 1rem;
}
.user_list_genre_container::-webkit-scrollbar{
    width: 7px;
}

.user_list_genre_container::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.user_list_genre_container::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.user_list_genre_container p{
    padding: 0;
    margin: 0;
    text-align: left;
}
.user_list_genre{
    color: #FBFFFE;
    background-color: grey;
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.6rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.4);
}
.add_friend_btn{
    margin: 0;
    padding: 0;
    all: unset;
    background-color: #FBFFFE;
    color: #1B1B1E;
    border: 3px solid #1B1B1E;
    font-weight: 700;
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.4rem;
    font-size: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.view_more_btn{
    all: unset;
    font-size: 1rem;
    align-self: center;
    text-decoration: underline;
}
.sort_filter_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 42rem;
}
.sort_by_container{
    width: 16rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.sort_button{
    all: unset;
    background-color: #FAA916;
    color: #1B1B1E;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.sort_button:hover{
    background-color: #faaa16bf;
    color: #1b1b1eb0;
}
.sort_select{
    display: flex;
    align-items: center;
    background-color: #FBFFFE;
    font-size: 1.1rem;
    width: 9rem;
    height: 2.5rem;
    border-radius: 0.5rem;
    border: 2px solid #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.filter_by_container{
    width: 24rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.filter_by_container input{
    all: unset;
    background-color: #FBFFFE;
    align-items: center;
    width: 3rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.filter_by_container label{
    font-weight: 500;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.reset_button{
    all: unset;
    margin-left: 0.9rem;
    background-color: #e51635;
    color: #FBFFFE;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;

}
.reset_button:hover{
    background-color: #e51635ca;
    color: #fbfffed1;
}
.filter_button{
    all: unset;
    background-color: #41ceaa;
    color: #1B1B1E;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.filter_button:hover{
    background-color: #41ceabd3;
    color: #1b1b1eb0;
}
.pagination_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 42rem;
}
.pagination_button{
    all: unset;
    font-weight: 500;
    font-size: 1.2rem;
    background-color: #FBFFFE;
    color: #1B1B1E;
    border: 3px solid #1B1B1E;
    border-radius: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.pagination_button:hover{
    background-color: #1B1B1E;
    color: #FBFFFE;
}
.pagination_button:disabled{
    background-color: #fbfffeb6;
    color: #1b1b1e74;
    border: 3px solid #1b1b1e74;
}

.other_user_modal{
    margin: 0;
    padding: 0;
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
.other_user_modal_container{
    background-color: #FBFFFE;
    width: 48rem;
    height: 38rem;
    padding: 3rem;
    padding-top: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
}
.other_user_modal_header{
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.other_user_modal_header h1{
    margin: 0;
}
.other_user_info_div{
    margin-top: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    font-size: 1.5rem;
    gap: 1rem;
}
.other_user_genre_container{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    max-height: 8rem;
    gap: 0.8rem;
    width: 100%;
    padding-left: 0.1rem;
    padding-bottom: 0.2rem;

}
.other_user_genre{
    color: #FBFFFE;
    background-color: grey;
    font-size: 1.4rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 0.9rem;
    padding-right: 0.9rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.other_user_book_container{
    margin: 0;
    padding: 0;
    width: 100%;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: flex-start;
    height: 15rem;
    max-height: 15rem;
    overflow-y: auto;
    padding-left: 1rem;
    padding-top: 0.3rem;
    padding-bottom: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.other_user_book_container::-webkit-scrollbar{
    width: 3px;
}

.other_user_book_container::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.other_user_book_container::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.other_user_book_li{
    width: 42%;
    padding: 1rem;
    background-color: #FBFFFE;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: 0.3s ease;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    height: 11rem;
    max-height: 11rem;
}
.other_user_book_li:hover{
    transform: scale(1.06);
}
.other_user_book_img{
    width: 7.3rem;
    height: 11rem;
    border-radius: 0.3rem;
}
.other_user_book_info_div{
    width: 12rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    font-size: 0.9rem;
    gap: 0.1rem;
}
.other_user_book_info_div p{
    margin: 0;
    padding: 0;
    text-align: left;
}
.other_user_book_info_title{
    max-height: 4rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.other_user_book_info_title::-webkit-scrollbar{
    width: 3px;
}

.other_user_book_info_title::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.other_user_book_info_title::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.other_user_book_info_authors{
    margin: 0;
    padding: 0;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    overflow-y: auto;
    max-height: 2.5rem;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.other_user_book_info_authors::-webkit-scrollbar{
    width: 3px;
}

.other_user_book_info_authors::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.other_user_book_info_authors::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.other_user_book_info_genres{
    margin: 0;
    padding: 0;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 0.3rem;
    max-height: 5rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.other_user_book_info_genres::-webkit-scrollbar{
    width: 3px;
}

.other_user_book_info_genres::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.other_user_book_info_genres::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.other_book_genre{
    font-size: 0.85rem;
    color: #FBFFFE;
    background-color: darkblue;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    padding-left: 0.3rem;
    padding-right: 0.3rem;
    border-radius: 0.3rem;
}
.other_book_more_info_btn{
    all: unset;
    margin: 0;
    padding: 0;
    align-self: center;
    margin-top: auto;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    padding-right: 2rem;
    padding-left: 2rem;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    border-radius: 0.3rem;
    font-weight: 400;
    transition: 0.3s ease;
}
.other_book_more_info_btn:hover{
    transform: scale(1.05);
    background-color: #41ceaa;
    font-weight: 500;
}
.more_info_book_div{
    margin-top: 1rem;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding-right: 1rem;
    overflow-y: auto;
    font-size: 1.05rem;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.more_info_book_div::-webkit-scrollbar{
    width: 3px;
}

.more_info_book_div::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.more_info_book_div::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.more_info_book_img{
    width: 11rem;
    height: 16.6rem;
    border-radius: 0.5rem;
}
.more_info_info_div{
    width: 35rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
    text-align: left;
}
.more_info_info_authors{
    width: 100%;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
}

.more_info_info_genres_container{
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.more_info_info_genre{
    padding: 0;
    margin: 0;
    background-color: darkblue;
    color: #FBFFFE;
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    padding-right: 0.6rem;
    padding-left: 0.6rem;
    border-radius: 0.4rem;
}

.back_btn{
    all: unset;
    margin-right: 1rem;
    background-color: #FAA916;
    color: #1B1B1E;
    font-weight: 500;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.back_btn:hover{
    background-color: #faaa16be;
    color: #1b1b1e8f;
}
.close_btn{
    all: unset;
    background-color: #e51635;
    color: #FBFFFE;
    font-weight: 500;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

.close_btn:hover{
    background-color: #e51635ba;
    color: #fbfffec9;
}
.social_page_nav{
    width: 38rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    height: 5rem;
}
.nav_btn_dashboard{
    all: unset;
    background-color: #FBFFFE;
    border: 3px solid #1B1B1E;
    font-weight: 500;
    color: #1B1B1E;
    font-size: 1.1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
    cursor: pointer;
}
.nav_btn_dashboard:hover{
    background-color: #1B1B1E;
    color: #FBFFFE;
}
.nav_btn_search_books{
    all: unset;
    background-color: #FBFFFE;
    border: 3px solid #1B1B1E;
    font-weight: 500;
    color: #1B1B1E;
    font-size: 1.1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
    cursor: pointer;
}
.nav_btn_search_books:hover{
    background-color: #1B1B1E;
    color: #FBFFFE;
}
.friend_request_container{
    margin-top: 2rem;
    padding: 0;
    padding: 2rem;
    padding-top: 0;
    width: 34rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    background-color: #FBFFFE;
    border-radius: 1rem;
}
.friend_request_btn_container{
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.friend_request_type_btns{
    display: flex;
    flex-direction: row;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 0.5rem;
}
.friend_request_type_button1{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #FAA916;
    border: 3px solid #FAA916;
    border-right: none;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}
.friend_request_type_button1:hover{
    border: 3px solid #ffc75f;
    border-right: none;
    color: #ffc75f;
}
.friend_request_type_button1:disabled{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #FAA916;
    border: 3px solid #FAA916;
    border-right: none;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}

.friend_request_type_button1.active{
    background-color: #FAA916;
    color: #FBFFFE;
}
.friend_request_type_button2{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #FAA916;
    border: 3px solid #FAA916;
    border-left: none;
    border-top-right-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}
.friend_request_type_button2.active{
    background-color: #FAA916;
    color: #FBFFFE;
}
.friend_request_type_button2:hover{
    border: 3px solid #ffc75f;
    border-left: none;
    color: #ffc75f;
}
.friend_request_type_button2:disabled{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #FBFFFE;
    border: 3px solid #FAA916;
    border-left: none;
    border-top-right-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    background-color: #FAA916;
    transition: 0.3s ease;
    font-weight: 500;
}

.friend_request_status_btns{
    display: flex;
    flex-direction: row;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 0.5rem;
}
.friend_request_status_button1{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #41ceaa;
    border: 3px solid #41ceaa;
    border-right: none;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}
.friend_request_status_button1:hover{
    border: 3px solid #67dec0;
    border-right: none;
    color: #67dec0;
}
.friend_request_status_button1:disabled{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #41ceaa;
    border: 3px solid #41ceaa;
    border-right: none;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}

.friend_request_status_button1.active{
    background-color: #41ceaa;
    color: #FBFFFE;
}
.friend_request_status_button2{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #41ceaa;
    border: 3px solid #41ceaa;
    border-left: none;
    border-top-right-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    background-color: #FBFFFE;
    transition: 0.3s ease;
    font-weight: 500;
}
.friend_request_status_button2.active{
    background-color: #41ceaa;
    color: #FBFFFE;
}
.friend_request_status_button2:hover{
    border: 3px solid #67dec0;
    border-left: none;
    color: #67dec0;
}
.friend_request_status_button2:disabled{
    all: unset;
    height: 1.9rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    color: #FBFFFE;
    border: 3px solid #41ceaa;
    border-left: none;
    border-top-right-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
    background-color: #41ceaa;
    transition: 0.3s ease;
    font-weight: 500;
}
.friend_request_ul{
    width: 100%;
    margin: 0;
    padding: 0;
    margin-top: 1rem;
    padding-left: 0.5rem;
    padding-bottom: 0.5rem;
    padding-top: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 13rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.friend_request_ul::-webkit-scrollbar{
    width: 5px;
}

.friend_request_ul::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.friend_request_ul::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.friend_request_li{
    width: 30rem;
    height: 3rem;
    border-radius: 0.4rem;
    padding-right: 1rem;
    padding-left: 1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.friend_request_ul1{
    margin: 0;
    padding: 0;
    width: 100%;
    padding-left: 0.5rem;
    padding-top: 0.3rem;
    padding-bottom: 0.5rem;
    margin-top: 1.2rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 1rem;
    max-height: 13rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.friend_request_ul1::-webkit-scrollbar{
    width: 5px;
}

.friend_request_ul1::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.friend_request_ul1::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.friend_request_li1{
    padding: 0;
    margin: 0;
    width: 14.5rem;
    height: 3rem;
    border-radius: 0.4rem;
    padding-right: 0.7rem;
    padding-left: 0.7rem;
    font-size: 1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.no_request_li{
    width: 14.5rem;
    font-size: 1.2rem;
    font-weight: 500;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.request_action_btns{
    width: 9rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.accept_btn{
    all: unset;
    background-color: rgb(7, 196, 7);
    color: #FBFFFE;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    padding-right: 0.6rem;
    padding-left: 0.6rem;
    border-radius: 0.3rem;
    font-weight: 400;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}
.accept_btn:hover{
    background-color: rgba(7, 196, 7, 0.713);
    color: #fbfffecd;
}
.decline_btn{
    all: unset;
    background-color: #e51635;
    color: #FBFFFE;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    padding-right: 0.4rem;
    padding-left: 0.4rem;
    border-radius: 0.3rem;
    font-weight: 400;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}
.decline_btn:hover{
    background-color: #e51635ab;
    color: #fbfffecd;
}


</style>