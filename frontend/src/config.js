/**
 * Application configuration
 */

// Get the base URL for API requests
// In production, use relative URLs (empty string)
// In development, use localhost
const getApiBaseUrl = () => {
  // If we're in production or running on a non-localhost domain
  if (window.location.hostname !== 'localhost' && 
      window.location.hostname !== '127.0.0.1') {
    return '';  // Empty string for relative URLs in production
  }
  
  // In development, use localhost
  return 'http://127.0.0.1:8000';
};

export const config = {
  apiBaseUrl: getApiBaseUrl()
};

export default config; 