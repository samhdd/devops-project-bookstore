// src/utils/imageUtils.js

// Import logo for fallback
import logo from '../assets/logo192.png';

/**
 * Get book cover image URL by book ID or image URL
 * 
 * This function accepts either:
 * 1. A direct image_url from the database (preferred) OR
 * 2. A book ID to build a URL as fallback
 * 
 * Uses database image_url directly when available for maximum scalability
 */
export function getBookCoverById(idOrImageUrl, bookData) {
  // Handle empty input
  if (!idOrImageUrl) {
    return logo;
  }
  
  try {
    // CASE 1: If bookData is provided and has an image_url, use that directly
    if (bookData && bookData.image_url) {
      // Always use the image URL from the database when available
      console.log(`Using database image URL: ${bookData.image_url}`);
      return bookData.image_url;
    }
    
    // CASE 2: If the passed parameter is already a complete URL/path from API, use it directly
    if (typeof idOrImageUrl === 'string' && (idOrImageUrl.startsWith('/api/') || idOrImageUrl.startsWith('http'))) {
      console.log(`Using provided API image path: ${idOrImageUrl}`);
      return idOrImageUrl;
    }
    
    // CASE 3: For backwards compatibility - construct path from id
    const id = idOrImageUrl.toString();
    // Use the API endpoint for images instead of direct file access
    const imageUrl = `/api/images/books/book-${id}.jpg`;
    console.log(`Constructed fallback image URL: ${imageUrl}`);
    
    return imageUrl;
  } catch (error) {
    console.error(`Error loading image for book ID ${idOrImageUrl}:`, error);
    return logo;
  }
}
