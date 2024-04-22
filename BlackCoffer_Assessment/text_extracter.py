import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


input_data = pd.read_excel("input.xlsx")

def extract_article_text(url, article_id):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the article element
        article = soup.find('article')

        # Check if the article element is found
        if article:
            # Find the article ID
            # article_id = url.split('/')[-2]  # Extract the second last part of the URL
            
            # Find the title of the article
            title_element = soup.find('h1', class_='entry-title') or soup.find('h1', class_='td-post-title') 
            if title_element:
                title = title_element.text.strip()
            else:
                title_element = soup.find('h1', class_='tdb-title-text')
                if title_element:
                    title = title_element.text.strip()
                else:
                    # print("Title not found.")
                    return None, None
            
            # Find the main content of the article
            content = soup.find('div', class_='td-post-content tagdiv-type')
            
            # Check if the content was found
            if content:
                # Find all paragraph elements within the main content
                paragraphs = content.find_all('p')
                
                # Extract text from paragraphs and concatenate them
                article_text = '\n'.join([p.get_text().strip() for p in paragraphs])
                
                # Create a folder named "articles" if it doesn't exist
                folder_name = "article_texts"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Save the extracted article text to a text file in the folder
                filename = os.path.join(folder_name, f"{article_id}.txt")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(article_text)
                # print(f"Article text saved to {filename}")

                return article_id, title, article_text
            else:
                # print(content)
                # print("Content not found with class 'td-post-content tagdiv-type'. Trying alternative class...")
                # Try finding the content using an alternative class
                # content = soup.find('div', class_='tdb-block-inner td-fix-index')
                # td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type
                content = soup.find('div', class_='td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
                # print(content)
                # Check if the alternative content was found
                if content:
                    # Find all paragraph elements within the alternative content
                    paragraphs = content.find_all('p')
                    
                    # Extract text from paragraphs and concatenate them
                    article_text = '\n'.join([p.get_text().strip() for p in paragraphs])
                    
                    # Create a folder named "articles" if it doesn't exist
                    folder_name = "article_texts"
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    # Save the extracted article text to a text file in the folder
                    filename = os.path.join(folder_name, f"{article_id}.txt")
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(article_text)
                    # print(f"Article text saved to {filename}")

                    return article_id, title, article_text
                else:
                    # print("Content not found with alternative class 'tdb-block-inner td-fix-index'.")
                    # print(content)
                    return None, None, None
        else:
            print("Article not found.", url)
            return None, None, None
    else:
        print("Failed to retrieve the webpage. for ", url)
        return None, None, None

# Extract URLs from the input Excel file
urls = input_data["URL"].tolist()

data = pd.DataFrame(columns=['URL_ID', 'URL'])

# Iterate over each URL and extract article text
for n, url in enumerate(urls):
    # print(f"Extracting article from {url}")
    article_id = f"blackassign{n}"
    _a, title, article_text = extract_article_text(url, article_id)
    data.loc[len(data)] = [article_id, url]
data.to_excel('URL.xlsx', index = False)
    # if article_id and title and article_text:
    #     print("Article ID:", article_id)
    #     print("Title:", title)
    #     print("Article Text:", article_text)
    #     print("\n")
    # else:
    #     print("Extraction failed for", url)


# the following two links are not working or do not exist
#Failed to retrieve the webpage. for  https://insights.blackcoffer.com/how-neural-networks-can-be-applied-in-various-areas-in-the-future/
# Failed to retrieve the webpage. for  https://insights.blackcoffer.com/covid-19-environmental-impact-for-the-future/