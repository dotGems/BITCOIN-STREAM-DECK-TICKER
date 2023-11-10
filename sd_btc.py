import requests
import os
import time
from config import sdFolderDir,d1,d2,d3,d4,d5,d6
from PIL import Image, ImageDraw, ImageFont

#Pulls the Bitcoin Price from coingecko
def get_bitcoin_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    data = response.json()
    return int(data['bitcoin']['usd'])

#Creates every digit of the price into a picture
def create_digit_images(price, folder_path, custom_names):
    size = 100
    font_size = 70
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    price_str = f"${price}"
    for index, digit in enumerate(price_str):
        img = Image.new('RGB', (size, size), color=(0, 0, 0))
        d = ImageDraw.Draw(img)

        # Calculate the bounding box of the text
        bbox = d.textbbox((0, 0), digit, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate X, Y position of the text
        x = (size - text_width) / 2
        y = (size - text_height) / 2

        d.text((x, y), digit, font=font, fill=(255, 255, 255))

        # Use custom name if index is less than the length of custom_names
        if index < len(custom_names):
            digit_image_path = os.path.join(folder_path, custom_names[index])
        else:
            digit_image_path = os.path.join(folder_path, f'digit_{index}.png')
        
        img.save(digit_image_path)
        print(f"Digit image for '{digit}' created at {digit_image_path}")

#places those pictures in the stream deck folder
if __name__ == "__main__":
    folder_path = os.path.expanduser(sdFolderDir)
    custom_names = [
        d1, d2, d3, d4, d5, d6
    ]
    
#runs the API price check every 60 seconds
    while True:  # Start an infinite loop
        try:
            price = get_bitcoin_price()
            create_digit_images(price, folder_path, custom_names)
        except requests.RequestException as e:
            print(f"An error occurred while fetching the Bitcoin price: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        time.sleep(60)  # Wait for 60 seconds before next execution
