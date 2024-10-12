import os
import requests
from serpapi import GoogleSearch

# Set up parameters for SerpAPI search
def fetch_squirrel_images(api_key, num_images=250):
    search_params = {
        "q": "pictures of squirrels on trees",
        "tbm": "isch",  # This sets the search to images
        "ijn": "0",     # Index number for the image results
        "api_key": api_key,
        "num": 200,     # Number of results per page
    }

    search = GoogleSearch(search_params)
    results = search.get_dict()

    # Create a directory for squirrel images
    if not os.path.exists('squirrel_images'):
        os.mkdir('squirrel_images')

    # Loop through results and download images
    for idx, image_info in enumerate(results['images_results'][:num_images]):
        image_url = image_info['original']
        try:
            # Download the image
            print(f"Downloading {image_url}")
            image_data = requests.get(image_url).content
            with open(f"squirrel_images/squirrel_tree_{idx}.jpg", 'wb') as handler:
                handler.write(image_data)
        except Exception as e:
            print(f"Could not download {image_url} due to {e}")
    
    print(f"Downloaded {num_images} squirrel images.")

# Example usage:
api_key = "9b9ebac856fbb9a8071cd35c7a6f450a01e3e02ab3dc123b3d08ed17c5f2a23c"  # Replace this with your actual SerpAPI key
fetch_squirrel_images(api_key, num_images=200)  # Adjust the number of images as needed
