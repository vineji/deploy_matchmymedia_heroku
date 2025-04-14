import { defineStore } from "pinia";

export const useUserStore = defineStore('userStore',{
    state: () => ({
        user_id : null,
        username : null,
        online_id : null,
        favourite_genres : []
    }),
    actions:{
        setUser(user_id, username, online_id, favourite_genres){
            this.user_id = user_id;
            this.username = username;
            this.online_id = online_id;
            this.favourite_genres = favourite_genres;
            localStorage.setItem('user', JSON.stringify(this.$state));
        },
        loadUser(){
            const user = localStorage.getItem('user');
            if (user){
                const parsedUser = JSON.parse(user);
                this.user_id = parsedUser.user_id;
                this.username = parsedUser.username;
                this.online_id = parsedUser.online_id;
                this.favourite_genres = parsedUser.favourite_genres;
            }
        },
        updateUsername(username){
            this.username = username;
        },
        updateOnlineID(online_id){
            this.online_id = online_id;
        },
        updateFavouriteGenres(favourite_genres){
            this.favourite_genres = favourite_genres;
        },
        clearUser(){
            localStorage.removeItem("user");
            sessionStorage.removeItem("user");
            this.user_id = null;
            this.username = null;
            this.online_id = null;
            this.favourite_genres = [];
        }
    }
})