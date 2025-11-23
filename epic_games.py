import requests
from datetime import datetime

EPIC_API_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

def get_epic_free_games():
    """
    Fetch current free games from Epic Games Store
    Returns a list of free game dictionaries
    """
    try:
        params = {
            'locale': 'en-US',
            'country': 'US',
            'allowCountries': 'US'
        }
        
        response = requests.get(EPIC_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        free_games = []
        
        # Parse the games data
        games = data.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', [])
        
        for game in games:
            # Check if game has promotional offers
            promotions = game.get('promotions')
            if not promotions:
                continue
            
            # Check both current and upcoming promotions
            promotional_offers = promotions.get('promotionalOffers', [])
            
            for offer_set in promotional_offers:
                for offer in offer_set.get('promotionalOffers', []):
                    # Check if it's currently free (discount price is 0)
                    discount_price = game.get('price', {}).get('totalPrice', {}).get('discountPrice', -1)
                    
                    if discount_price == 0:
                        # Extract game information
                        title = game.get('title', 'Unknown Game')
                        description = game.get('description', 'No description available')
                        
                        # Build the store URL
                        product_slug = game.get('productSlug') or game.get('catalogNs', {}).get('mappings', [{}])[0].get('pageSlug', '')
                        url = f"https://store.epicgames.com/en-US/p/{product_slug}" if product_slug else "https://store.epicgames.com"
                        
                        # Get end date
                        end_date_str = offer.get('endDate', '')
                        try:
                            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                            end_date_formatted = end_date.strftime('%B %d, %Y at %I:%M %p UTC')
                        except:
                            end_date_formatted = 'Unknown'
                        
                        # Get original price
                        original_price = game.get('price', {}).get('totalPrice', {}).get('originalPrice', 0)
                        original_price_formatted = f"${original_price / 100:.2f}" if original_price > 0 else "Free"
                        
                        # Get image
                        images = game.get('keyImages', [])
                        image_url = None
                        for img in images:
                            if img.get('type') in ['DieselStoreFrontWide', 'OfferImageWide', 'Thumbnail']:
                                image_url = img.get('url')
                                break
                        
                        # Create unique ID
                        game_id = game.get('id', product_slug)
                        
                        free_games.append({
                            'id': game_id,
                            'title': title,
                            'description': description,
                            'url': url,
                            'end_date': end_date_formatted,
                            'original_price': original_price_formatted,
                            'image': image_url
                        })
        
        # Remove duplicates based on ID
        seen_ids = set()
        unique_games = []
        for game in free_games:
            if game['id'] not in seen_ids:
                seen_ids.add(game['id'])
                unique_games.append(game)
        
        return unique_games
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Epic Games data: {e}")
        return []
    except Exception as e:
        print(f"Error parsing Epic Games data: {e}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing Epic Games API...")
    games = get_epic_free_games()
    
    if games:
        print(f"\nFound {len(games)} free game(s):\n")
        for game in games:
            print(f"Title: {game['title']}")
            print(f"URL: {game['url']}")
            print(f"End Date: {game['end_date']}")
            print(f"Original Price: {game['original_price']}")
            print("-" * 50)
    else:
        print("No free games found or error occurred.")
