<template>
    <div v-if="isVisible" class="modal-container">
        <div class="modal">
            <div class="modal-header">
                <p>Recommended books for: {{ mediaType }} - {{ mediaName }}</p>
                <div>
                    <button v-if="show_list == false" @click="back" class="back">Back</button>
                    <button @click="close" class="close-button">Close</button>
                </div>
            </div>
            <ul v-if="show_list" class="list-container">
                <li class="loading" v-if="recommendedBooks.length == 0"> Loading...</li>
                <li class="books_li" v-for="book in recommendedBooks" :key="book.title">
                    <img :src="book.image" class="book_image">
                    <div class="books_li_container">
                        <div class="books_li_div">
                            <p class="book_div_title"><b>Title: </b>{{ book.title || "Unavailable" }}</p>
                            <p><b>Published: </b>{{ book.published_date || "Unavailable" }}</p>
                            <div class="books_li_authors">
                                <p><b>Authors: </b></p>
                                <li style="padding-right: 0.3rem;" v-if="book?.authors?.length == 0">Unknown</li>
                                <li style="padding-right: 0.3rem;" v-for="(author,index) in book.authors" :key="index">
                                    <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                </li>
                            </div>
                            <div class="books_li_categories">
                                <p><b>Categories:</b></p>
                                <ul v-if="book.categories.length > 0" class="category_ul">
                                    <li class="rcmnd_genre" style="background-color: darkblue;" v-for="category in book.categories" :key="category">{{ category }}</li>
                                </ul>
                                <ul v-else>
                                    <li  style="background-color: #9b9a9a;">Unknown</li>
                                </ul>
                            </div>
                        </div>
                        <button class="more_info" @click="more_info(book)">More info</button>
                    </div>
                </li>
            </ul>
            <div v-if="show_list == false" class="chosen_book_div">
                <div class="chosen_book_container">
                    <img :src="chosen_book.image" class="chosen_book_image">
                    <div class="chosen_book_div1">
                        <div class="div1_title">
                            <p class="chosen_book_div1_title"><b>Title: </b>{{ chosen_book.title || "Unavailable" }}</p>
                            <button class="fav_btn_modal" @click="addToFavourites()">Add to Favourites</button>
                        </div>
                        <ul class="chosen_book_authors">
                            <div class="chosen_book_authors_div">
                                <p><b>Authors: </b></p>
                                <li style="padding-right: 0.3rem;" v-if="chosen_book?.authors?.length == 0">Unknown</li>
                                <li v-for="(author,index) in chosen_book?.authors" :key="index">
                                    <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                </li>
                            </div>
                            <div class="star_rating_div_modal">
                                <p>Your rating: </p>
                                <button
                                v-for="star in stars"
                                :key="star"
                                @click="rateBook(star)"
                                @mouseover="hoverStar(star)"
                                @mouseleave="resetHover"
                                :class="['star_modal',{hovered: hoveredStar >= star, filled: rating >= star}]"
                                >
                                <span v-html="hoveredStar >= star || rating >= star ? '&#9733;' : '&#9734;'"></span>
                                </button>
                            </div>
                        </ul>
                        <p><b>Published Date: </b>{{ chosen_book.published_date || "Unavailable" }}</p>
                        <ul v-if="chosen_book.categories.length > 0" class="chosen_genre_list">
                            <p><b>Categories: </b> </p>
                            <li class="chosen_genre" style="background-color: grey;" v-for="category in chosen_book.categories" :key="category">{{ category}}</li>
                        </ul>
                        <ul v-else class="chosen_genre_list">
                            <p><b>Categories: </b> </p>
                            <li class="chosen_genre" style="background-color: #9b9a9a;">Unknown</li>
                        </ul>
                        <p><b>Description: </b>{{ chosen_book.description || "Unavailable" }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>



export default{
    data()  {
        return{
            show_list : true,
            chosen_book : null,
            csrfToken : "",
            stars : [1,2,3,4,5],
            rating : 0,
            hoveredStar : 0,
        }

    },
    props: ['recommendedBooks','isVisible','mediaType','mediaName', "loggedUser"],
    watch: {
        isVisible(newVal){
            if (newVal) {
                this.show_list = true;
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
        async addToFavourites(){
            if (this.loggedUser){
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
                }
                catch (error){
                    console.error("Error adding book:", error);
                }
            }
            else{
                alert("You have to have an account to favourite a book.");
            }

        },
        async fetch_book_rating(){
            if (this.loggedUser){
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
            }
        },
        async rateBook(rating){

            if (this.loggedUser){
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
        close(){
            this.$emit('update:isVisible', false);
        },
        more_info(book){
            this.show_list = false;
            this.chosen_book = book;
            this.fetch_book_rating();
        },
        back(){
            this.show_list = true;
        }
    },
    mounted(){
        this.fetch_csrf_token();
    }
}
</script>
<style>
.loading{
    align-self: center;
    justify-self: center;
}
.modal-container{
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
.modal{
    background-color: #FBFFFE;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 75rem;
    max-width: 75rem;
    height: 40rem;
    max-height: 40rem;
    border-radius: 1rem;

}
.list-container{
    height: 30rem;
    max-height: 30rem;
    width: 65rem;
    max-width: 65rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    gap: 1rem;
    padding-bottom: 1rem;
    padding-top: 0.5rem;
}

.list-container::-webkit-scrollbar{
    width: 0.5rem;
}

.list-container::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 2rem;
}
.list-container::-webkit-scrollbar-track{
    background-color: #e9e7e7;
    border-radius: 2rem;
}
.modal-header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 93%;
    margin-left: 1rem;
    justify-self: flex-start;
}
.books_li_container{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 12rem;
}
.books_li{
    display: flex;
    flex-direction: row;
    width: 18rem;
    max-width: 18rem;
    max-height: 12rem;
    font-size: 0.85rem;
    padding: 1rem;
    gap: 0.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

.books_li:hover{
    transform: scale(1.06);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.books_li_div{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    height: 10.5rem;

}
.books_li p{
    gap: 0;
    margin: 0;
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.book_image{
    height: 12rem;
    width: 8rem;
    max-width: 8rem;
    border-radius: 0.3rem;
}
.category_ul{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0;
    padding: 0;
}
.book_div_title{
    max-height: 6rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    width: 9.5rem;
    padding-right: 0.1rem;
}

.book_div_title::-webkit-scrollbar{
    width: 3px;
}

.book_div_title::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.book_div_title::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_authors{
    width: 9.6rem;
    max-height: 2.3rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
}
.books_li_authors p{
    padding-right: 0.3rem;
}
.books_li_authors::-webkit-scrollbar{
    width: 3px;
}

.books_li_authors::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_authors::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}

.books_li_categories{
    width: 9.6rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    max-height: 5rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
}
.books_li_categories::-webkit-scrollbar{
    width: 3px;
}

.books_li_categories::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_categories::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_categories p{
    padding-right: 0.3rem;
}

.rcmnd_genre{
    display: inline-block;
    color: #FBFFFE;
    padding-right: 0.3rem;
    padding-left: 0.3rem;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    border-radius: 0.3rem;
    max-width: 8rem;
    font-size: 0.8rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.more_info{
    align-self: center;
    justify-self: flex-end;
    width: 8rem;
    height: 1.3rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    transition: 0.2s ease;
}

.more_info:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.close-button{
    all: unset;
    width: 4rem;
    height: 3rem;
    font-size: 1.2rem;
    border: none;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    border-radius: 0.5rem;
    color: #FBFFFE;
    background-color: #e51635;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.close-button:hover{
    font-weight: 600;
    background-color: #fc2646;
    transition: ease 0.3s;
}
.chosen_book_div{
    min-height: 31.5rem;
    max-height: 31.5rem;
    width: 67.5rem;
    margin: 1rem;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}
.chosen_book_div::-webkit-scrollbar{
    width: 0.5rem;
}

.chosen_book_div::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 2rem;
}
.chosen_book_div::-webkit-scrollbar-track{
    background-color: #e9e7e7;
    border-radius: 2rem;
}
.chosen_book_container{
    display: flex;
    flex-direction: row;
    width: 55rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    border-radius: 1rem;
    padding: 2rem;
    margin-top: 0.7rem;
    margin-bottom: 0.5rem;
}
.chosen_book_div1{
    display: flex;
    width: 40rem;
    flex-direction: column;
    align-items: flex-start;
    margin-left: 1rem;
    min-height: 10rem;
}
.chosen_book_div1 p{
    gap: 0%;
    padding: 0%;
    margin: 0%;
    text-align: left;
}
.chosen_book_div1_title{
    width: 30rem;
    max-width: 30rem;
}
.div1_title{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;

}
.fav_btn_modal{
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
.fav_btn_modal:hover{
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.chosen_book_authors{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0;
    width: 40rem;
}
.chosen_book_authors_div{
    display: flex;
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
    padding: 0;
    gap: 0.5rem;
    width: 25rem;
}
.chosen_book_image{
    height: 21rem;
    width: 15rem;
    max-width: 15rem;
    border-radius: 0.7rem;
}
.back{
    border: 3px solid #FAA916;
    color: #FAA916;
    background-color: #FBFFFE;
    font-weight: 401;
    font-size: 1.2rem;
    margin-right: 1.5rem;
    padding-right: 1rem;
    padding-left: 1rem;
    border-radius: 0.5rem;
    height: 2.99rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.back:hover{
    background-color: #FAA916;
    color: #FBFFFE;
    transition: 0.3s ease;
}
.loading{
    align-self: center;
    margin-left: auto;
    margin-right: auto;
    font-size: 5rem;
    margin-bottom: 3rem;
    text-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.star_rating_div_modal{
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 14rem;
}
.star_rating_div_modal p{
    font-size: 1rem;
    margin-right: 0.5rem;
    font-weight: 501;
}
.star_modal{
    all: unset;
    background: none;
    border: none;
    font-size: 1.5rem;
    font-weight: 601;
    cursor: pointer;
    color: #FAA916;
}
.star_modal:hover{
    color: #FAA916;
}
.star_modal.filled{
    color: #FAA916;
}
</style>