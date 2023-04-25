
import os
import asyncio
from dotenv import load_dotenv


class ImageSearch:
    """Image search class
    via Flickr api custom search api"""

    def __init__(self):
        load_dotenv(dotenv_path="./token.env")
        TOKEN = "FLICKR_KEY"
        api_key = os.environ[TOKEN]
        self.api_key = api_key
        self.url = "https://live.staticflickr.com/"

    async def fetch_image(self, session, url: str) -> list:
        async with session.get(url) as response:
            return await response.json()
        
    async def search_image(self, session, query: str):
        """
        search_image loads images URL`s via API

        formed url can be used as the ilustrations

        Args:
            session (aiohttp instance): Session encapsulates 
            a connection pool (connector instance) and supports keepalives
            query (str): param for search query

        Returns:
            list: list of urls
        """
        endpoint = "https://api.flickr.com/services/rest/"
        params = {
            "method": "flickr.photos.search",
            "api_key": self.api_key,
            "text": query,
            "format": "json",
            "nojsoncallback": True
        }
        url = endpoint + '?' + '&'.join([f'{key}={value}' for key, value
                                        in params.items()])
        response = await self.fetch_image(session, url)
        photos = response["photos"]["photo"]
        image_urls = [f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg" for photo in photos]
        return image_urls
    
    # it is better to fix this method
    async def download_images(self, session, image_urls):
        tasks = []

        for i, image_url in enumerate(image_urls):
            tasks.append(asyncio.create_task(self.fetch_image(session, image_url)))
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            image_url = f"https://live.staticflickr.com/{result['server']}/{result['id']}_{result['secret']}.jpg"
            print(image_url)
            async with session.get(image_url) as response:
                with open(f'image_{i}.jpg', 'wb') as f:
                    f.write(await response.content.read())

        