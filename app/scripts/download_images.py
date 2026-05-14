import os
import requests
import logging
import shutil
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample stadium image URLs (using free-to-use images)
STADIUM_IMAGES = {
    'stadium1.jpg': 'https://images.pexels.com/photos/2740956/pexels-photo-2740956.jpeg',  # Modern stadium
    'stadium2.jpg': 'https://images.pexels.com/photos/2740954/pexels-photo-2740954.jpeg',  # Olympic stadium
    'stadium3.jpg': 'https://images.pexels.com/photos/2740955/pexels-photo-2740955.jpeg',  # Community stadium
    'stadium4.jpg': 'https://images.pexels.com/photos/2740957/pexels-photo-2740957.jpeg',  # Indoor arena
    'stadium5.jpg': 'https://images.pexels.com/photos/2740958/pexels-photo-2740958.jpeg',  # Football stadium
    'stadium6.jpg': 'https://images.pexels.com/photos/2740959/pexels-photo-2740959.jpeg',  # Concert venue
    'event1.jpg': 'https://images.pexels.com/photos/2740956/pexels-photo-2740956.jpeg',  # Music festival
    'event2.jpg': 'https://images.pexels.com/photos/2740954/pexels-photo-2740954.jpeg',  # Football match
    'event3.jpg': 'https://images.pexels.com/photos/2740955/pexels-photo-2740955.jpeg',  # Basketball game
    'event4.jpg': 'https://images.pexels.com/photos/2740957/pexels-photo-2740957.jpeg',  # Rock concert
    'event5.jpg': 'https://images.pexels.com/photos/2740958/pexels-photo-2740958.jpeg',  # Cricket match
    'event6.jpg': 'https://images.pexels.com/photos/2740959/pexels-photo-2740959.jpeg',  # Classical concert
    'indexstadium.jpg': 'https://images.pexels.com/photos/2740956/pexels-photo-2740956.jpeg',  # Home page background
    'loginstadium.jpg': 'https://images.pexels.com/photos/2740954/pexels-photo-2740954.jpeg'  # Login page background
}

def download_images():
    try:
        # Get the absolute path to the uploads directory
        base_dir = Path(__file__).parent.parent.parent
        uploads_dir = base_dir / 'app' / 'static' / 'uploads'
        
        # Remove existing uploads directory and recreate it
        if uploads_dir.exists():
            logger.info("Removing existing uploads directory...")
            shutil.rmtree(uploads_dir)
        
        logger.info("Creating new uploads directory...")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        for filename, url in STADIUM_IMAGES.items():
            target_path = uploads_dir / filename
            
            logger.info(f"Downloading {filename}...")
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Verify that we got an image
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    raise ValueError(f"Expected image content type, got {content_type}")
                
                with open(target_path, 'wb') as f:
                    f.write(response.content)
                
                # Verify the file was written and has content
                if target_path.stat().st_size < 1000:  # Less than 1KB is probably not an image
                    raise ValueError(f"Downloaded file {filename} is too small to be an image")
                
                logger.info(f"Successfully downloaded {filename} ({target_path.stat().st_size} bytes)")
                
            except Exception as e:
                logger.error(f"Failed to download {filename}: {str(e)}")
                if target_path.exists():
                    target_path.unlink()
                raise
        
        logger.info("All images downloaded successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        download_images()
    except Exception as e:
        logger.error(f"Failed to download images: {str(e)}")
        exit(1) 