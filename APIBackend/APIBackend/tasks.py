# from .email import send_otp_mail
from celery.utils.log import get_task_logger
from celery import shared_task
from SentimentAnalysis.serializers import AdditionSerializer,ReviewsSerializer
import datetime
from rest_framework import response, status
#scrapping data with beautifulsoup
from bs4 import BeautifulSoup
import requests
import csv


logger = get_task_logger(__name__)


@shared_task(name='APIBackend.tasks.add_two_numbers')
def add_two_numbers(a, b):
    logger.info('add two numbers')
    #store the result in the database
    try:
        result = a + b
        # my_object = {"num_1":a, "num_2":b, "result":result,"date" : datetime.datetime.now()}
        my_object = {"num_1":a, "num_2":b, "result":result}
        # print(my_object)
        
        serializer = AdditionSerializer(data=my_object)
        # print(serializer)
        if serializer.is_valid():
            # print("serializer is valid")
            serializer.save()
        else:
            print("serializer is not paused ")
            # return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return result
    except Exception as e:
        print("error", e)
        return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@shared_task(name='APIBackend.tasks.divide_two_numbers')
def divide_two_numbers(a, b):
    logger.info('dividing two numbers')
    return a / b


@shared_task(name='APIBackend.tasks.scrap_data_with_beautifulsoup')
def scrap_data_with_beautifulsoup(web_url):
    page_to_scrape = requests.get(web_url)
    soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    # print(soup.prettify())
    # return soup.prettify()
    quotes =soup.find_all('span', attrs={'class':'text'})
    authors =soup.find_all('small', attrs={'class':'author'})
    tag =soup.find_all('a', attrs={'class':'tag'})
    
    file = open('quotes.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['Quote', 'Author', 'Tags'])
    for i in range(0, len(quotes)):
        writer.writerow([quotes[i].text, authors[i].text, tag[i].text])
    file.close()
    
# @shared_task(name='APIBackend.tasks.scrap_data_from_site')
# def scrap_data_from_site(web_url):
#     page_to_scrape = requests.get(web_url)
#     soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
#     print(soup.prettify())
    # review_div = soup.find('div', class_='fIrGe')
    
    # if review_div:
    #     # Find the span with the specific class within the div
    #     review_span = review_div.find('span', class_='QewHA')
        
    #     if review_span:
    #         # Extract the text from the inner span
    #         review_text = review_span.find('span').text.strip()
    #         print(review_text)
    #         return review_text

@shared_task(name='APIBackend.tasks.scrap_data_from_site')
def scrap_data_from_site(web_url):
    page_to_scrape = requests.get(web_url)
    soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    
    # Find the 'a' tag with the specified class
    review_links = soup.find_all('a', class_='w-full hover:bg-foreground-50 transition-all rounded-xl p-6 border border-foreground-100')
    
    reviews = []
    for link in review_links:
        # Find the 'h1' element for the header
        header = link.find('h1', class_='text-lg font-semibold font-heading my-4 inline-block transition-all')
        # Find the 'p' element for the description
        description = link.find('p', class_='whitespace-pre-wrap w-full line-clamp-1')
        
        if header and description:
            reviews.append({
                'header': header.text.strip(),
                'description': description.text.strip()
            })
    
    # Print or return the reviews
    for review in reviews:
        print(review['header'])
        print(review['description'])
        try:
            my_object = {"source":"travel-review-site", "source_link":web_url, "title":review['header'], "description":review['description']}
            serializer = ReviewsSerializer(data=my_object)
            if serializer.is_valid():
                serializer.save()
            else:
                print("serializer is not paused ")
            return serializer.data
        except Exception as e:
            print("error", e)
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    # return reviews
    
#     @shared_task(name='APIBackend.tasks.scrap_data_from_site')
# def scrap_data_from_site(web_url):
#     page_to_scrape = requests.get(web_url)
#     soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    
#     # Find the 'a' tag with the specified class
#     review_links = soup.find_all('a', class_='w-full hover:bg-foreground-50 transition-all rounded-xl p-6 border border-foreground-100')
    
#     reviews = []
#     for link in review_links:
#         # Find the 'h1' element for the header
#         header = link.find('h1', class_='text-lg font-semibold font-heading my-4 inline-block transition-all')
#         # Find the 'p' element for the description
#         description = link.find('p', class_='whitespace-pre-wrap w-full line-clamp-1')
#         # Get the URL from the 'href' attribute
#         url = link['href']
        
#         if header and description:
#             reviews.append({
#                 'header': header.text.strip(),
#                 'description': description.text.strip(),
#                 'url': url
#             })
    
#     # Print or return the reviews
#     for review in reviews:
#         print(review['header'])
#         print(review['description'])
#         print(review['url'])
    
#     return reviews