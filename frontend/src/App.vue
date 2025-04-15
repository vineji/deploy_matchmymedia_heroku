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
    
    // Check if user session is valid at application startup
    const validateUserSession = async () => {
      const storedUser = localStorage.getItem('user');
      
      if (storedUser) {
        try {
          const response = await fetch(`${apiBaseUrl}/user/`, {
            method: "GET",
            credentials: "include"
          });
          
          if (!response.ok) {
            // If API call fails, clear the user store
            console.log('Session invalid, clearing stored user data');
            userStore.clearUser();
          }
        } catch (error) {
          console.error('Error validating user session:', error);
          userStore.clearUser();
        }
      }
    };
    
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
