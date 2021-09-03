#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image 
from IPython.display import display 
import random
import json


# In[2]:


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Orange", "Red", "Yellow"] 
background_weights = [20, 40, 40]

base = ["DarkBlue", "LightBlue", "MediumBlue", "Purple"] 
base_weights = [30, 30, 30, 10]

fur = ["GreyBlue","Pink", "SkyBlue", "White"] 
fur_weights = [30, 30, 30, 10]

eye = ["glasses", "normal"]
eye_weights = [30, 70]

# Dictionary variable for each trait. 
# Eech trait corresponds to its file name
# Add more shapes and colours as you wish

background_files = {
    "Orange": "Orange",
    "Red": "Red",
    "Yellow": "Yellow"
}

base_files = {
    "DarkBlue": "DarkBlue",
    "LightBlue": "LightBlue",
    "MediumBlue": "MediumBlue",
    "Purple": "Purple"
}

fur_files = {
    "GreyBlue": "GreyBlue",
    "Pink": "Pink", 
    "SkyBlue": "SkyBlue",
    "White": "White"
}

eye_files = {
    "glasses": "glasses",
    "normal": "normal"
}


# In[3]:


TOTAL_IMAGES = 96 # Number of random unique images we want to generate ( 3 x 4 x 4 x 2 = 8)

all_images = [] 

def create_new_image():

    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image ["Background"] = random.choices(background, background_weights)[0]
    new_image ["Base"] = random.choices(base, base_weights)[0]
    new_image ["Fur"] = random.choices(fur, fur_weights)[0]
    new_image ["Eye"] = random.choices(eye, eye_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


# In[4]:


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))


# In[5]:


i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1


# In[6]:


print(all_images)


# In[7]:


background_count = {}
for item in background:
    background_count[item] = 0

base_count = {}
for item in base:
    base_count[item] = 0

fur_count = {}
for item in fur:
    fur_count[item] = 0
    
eye_count = {}
for item in eye:
    eye_count[item] = 0

for image in all_images:
    background_count[image["Background"]] += 1
    base_count[image["Base"]] += 1
    fur_count[image["Fur"]] += 1
    eye_count[image["Eye"]] += 1

print(background_count)
print(base_count)
print(fur_count)
print(eye_count)


# In[8]:


METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


# In[9]:


for item in all_images:

    im1 = Image.open(f'./layers/backgrounds/{background_files[item["Background"]]}.png').convert('RGBA')
    im2 = Image.open(f'./layers/bases/{base_files[item["Base"]]}.png').convert('RGBA')
    im3 = Image.open(f'./layers/furs/{fur_files[item["Fur"]]}.png').convert('RGBA')
    im4 = Image.open(f'./layers/eyes/{eye_files[item["Eye"]]}.png').convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)

    #Convert to RGB
    rgb_im = com3.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)


# In[10]:


f = open('./metadata/all-traits.json',) 
data = json.load(f)

IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "CozyYety"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + '#' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Base", i["Base"]))
    token["attributes"].append(getAttribute("Fur", i["Fur"]))
    token["attributes"].append(getAttribute("Eye", i["Eye"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()


# In[ ]:




