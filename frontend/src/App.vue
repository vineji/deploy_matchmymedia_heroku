<template>
  <router-view></router-view>
</template>

<script>
import { useUserStore } from '@/stores/userStore';
import config from '@/config';

export default {
  name: 'App',
  setup() {
    const userStore = useUserStore();
    const apiBaseUrl = config.apiBaseUrl;
    
    // More aggressive check for user session validity
    const validateUserSession = async () => {
      try {
        const response = await fetch(`${apiBaseUrl}/user/`, {
          method: "GET",
          credentials: "include"
        });
        
        if (!response.ok) {
          // If API call fails, clear the user store
          console.log('Session invalid, clearing stored user data');
          userStore.clearUser();
        } else {
          // If successful, update the user data
          const userData = await response.json();
          userStore.setUser(userData.id, userData.username, userData.online_id, userData.favourite_genres);
        }
      } catch (error) {
        console.error('Error validating user session:', error);
        userStore.clearUser();
      }
    };
    
    // Always validate on app startup
    validateUserSession();
    
    return { userStore };
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
</style>
