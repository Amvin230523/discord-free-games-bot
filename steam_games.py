import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_steam_free_games():
    """
    Fetch temporarily free games from Steam
    Returns a list of free game dictionaries
    """
    free_games = []
    
    # Method 1: Check Steam's search for games that are 100% off
    try:
        search_url = "https://store.steampowered.com/search/?maxprice=free&specials=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'birthtime=0; mature_content=1'  # To avoid age gate
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find game entries
        game_entries = soup.find_all('a', class_='search_result_row')
        
        for entry in game_entries[:10]:  # Limit to first 10 results
            try:
                # Get game title
                title_elem = entry.find('span', class_='title')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                
                # Get game URL and ID
                game_url = entry.get('href', '').split('?')[0]  # Remove query params
                app_id = entry.get('data-ds-appid', '')
                
                # Check if it's actually free (was paid, now free)
                price_elem = entry.find('div', class_='discount_final_price')
                discount_elem = entry.find('div', class_='discount_pct')
                
                if not price_elem:
                    continue
                
                price_text = price_elem.text.strip()
                discount_pct = discount_elem.text.strip() if discount_elem else ''
                
                # Look for "Free" or games with 100% discount
                is_free = 'Free' in price_text or price_text == ''
                is_full_discount = '-100%' in discount_pct
                
                if is_free or is_full_discount:
                    # Get original price
                    original_price_elem = entry.find('div', class_='discount_original_price')
                    original_price = original_price_elem.text.strip() if original_price_elem else 'Paid Game'
                    
                    # Get game image
                    img_elem = entry.find('img')
                    image_url = img_elem.get('src', '') if img_elem else None
                    
                    # Get release date info (approximate end date)
                    released_elem = entry.find('div', class_='search_released')
                    released_text = released_elem.text.strip() if released_elem else ''
                    
                    # Try to extract description from review snippet
                    review_elem = entry.find('span', class_='search_review_summary')
                    description = review_elem.get('data-tooltip-html', 'Limited time free promotion!') if review_elem else 'Limited time free promotion!'
                    
                    # Clean up description (remove HTML)
                    description = BeautifulSoup(description, 'html.parser').get_text() if '<' in description else description
                    description = description[:200] + "..." if len(description) > 200 else description
                    
                    # Only add games that appear to be temporarily free (have original price)
                    if original_price and original_price != 'Paid Game':
                        free_games.append({
                            'id': f"steam_{app_id}",
                            'title': title,
                            'description': description,
                            'url': game_url,
                            'end_date': 'Check Steam page for end date',
                            'original_price': original_price,
                            'image': image_url
                        })
            except Exception as e:
                print(f"Error parsing Steam game entry: {e}")
                continue
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Steam data: {e}")
    except Exception as e:
        print(f"Error parsing Steam data: {e}")
    
    # Method 2: Check SteamDB's weekend deals (optional fallback)
    # Note: This is a simplified approach. For production, you might want to use SteamDB RSS or API if available
    
    return free_games

def get_steam_weekend_free():
    """
    Check for Steam's Free Weekend games
    These are separate from the 100% off promotions
    """
    free_weekend_games = []
    
    try:
        # Steam's free weekend page
        url = "https://store.steampowered.com/search/?category1=998&category2=21"  # Free to Play filter
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'birthtime=0; mature_content=1'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for "Free Weekend" tags
        game_entries = soup.find_all('a', class_='search_result_row')
        
        for entry in game_entries:
            try:
                # Check if it mentions "Free Weekend"
                text_content = entry.get_text()
                if 'Free Weekend' in text_content or 'Play for Free' in text_content:
                    title_elem = entry.find('span', class_='title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    game_url = entry.get('href', '').split('?')[0]
                    app_id = entry.get('data-ds-appid', '')
                    
                    img_elem = entry.find('img')
                    image_url = img_elem.get('src', '') if img_elem else None
                    
                    free_weekend_games.append({
                        'id': f"steam_weekend_{app_id}",
                        'title': f"{title} (Free Weekend)",
                        'description': 'Play for free this weekend! Check Steam for exact end time.',
                        'url': game_url,
                        'end_date': 'Check Steam page',
                        'original_price': 'Full Game Access',
                        'image': image_url
                    })
            except Exception as e:
                print(f"Error parsing Free Weekend game: {e}")
                continue
    
    except Exception as e:
        print(f"Error fetching Free Weekend games: {e}")
    
    return free_weekend_games

# Test function
if __name__ == "__main__":
    print("Testing Steam scraper...")
    print("\n=== Checking for 100% off games ===")
    games = get_steam_free_games()
    
    if games:
        print(f"\nFound {len(games)} temporarily free game(s):\n")
        for game in games:
            print(f"Title: {game['title']}")
            print(f"URL: {game['url']}")
            print(f"Original Price: {game['original_price']}")
            print("-" * 50)
    else:
        print("No temporarily free games found.")
    
    print("\n=== Checking for Free Weekend games ===")
    weekend_games = get_steam_weekend_free()
    
    if weekend_games:
        print(f"\nFound {len(weekend_games)} free weekend game(s):\n")
        for game in weekend_games:
            print(f"Title: {game['title']}")
            print(f"URL: {game['url']}")
            print("-" * 50)
    else:
        print("No free weekend games found.")
