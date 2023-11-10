from PIL import Image, ImageDraw, ImageFont
import requests
import os
import time  # Import the time module
from config import sdFolderDir

#NOTES
# STEP 1 : Setup Stream deck with 7 Fake Icons, [SYSTEM>OPEN]
# STEP 2 : Find where the icons are stored on your computer, streamdeck will rename them, you need the associated new file names.
# STEP 3 : open terminal, type "cd" then a space ... then drag and drop the folder where this .py file is stored. (this points terminal directory to your program)
# STEP 4 : Run Program -> Terminal command : python sd_btc.py

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
#MAC PATH TO STREAM DECK >Profiles>PROFILE>Images>" --- #stream deck auto renames your set images, copy genrated names to replace "custom_names" below
    folder_path = os.path.expanduser(sdFolderDir)
    custom_names = [
        "TTQM3OKFAP77L4VT0JVFMPVR5SZ.png",
        "SH1LFQM1TD6E73IEDKQD38FH9CZ.png",
        "PC4LAN6J0T04BA1BCGHTNEVLDKZ.png",
        "A9AV0TB4SH2HW5SVWJVIP31AP0Z.png",
        "0NWSRVBHL95OW1QT1A8NDJJKFGZ.png",
        "FDT33001LL0DF5E84IMFCQJL8KZ.png"
    ]
#runs the API price check every 5 seconds
    while True:  # Start an infinite loop
        try:
            price = get_bitcoin_price()
            create_digit_images(price, folder_path, custom_names)
        except requests.RequestException as e:
            print(f"An error occurred while fetching the Bitcoin price: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        time.sleep(5)  # Wait for 5 seconds before next execution
