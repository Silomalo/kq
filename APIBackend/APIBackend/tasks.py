# from .email import send_otp_mail
from celery.utils.log import get_task_logger
from celery import shared_task
from SentimentAnalysis.serializers import AdditionSerializer
# from APIBackend.SentimentAnalysis.models import Addition
import datetime
from rest_framework import response, status

#scrapping data with beautifulsoup
from bs4 import BeautifulSoup
import requests
import csv

logger = get_task_logger(__name__)


# @task(name='send_otp_mail')
# def send_otp_mail_task(time_otp, mail_id):
#     logger.info('send otp')
#     return send_otp_mail(time_otp, mail_id)

# @shared_task(name='add_two_numbers')
# @shared_task()
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
    
@shared_task(name='APIBackend.tasks.scrap_data_from_site')
def scrap_data_from_site(web_url):
    page_to_scrape = requests.get(web_url)
    soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
    title_element = soup.find('span', class_='Qwuub')
    description_element = soup.find('span', class_='QewHA H4 *a')
    print(description_element)
    if title_element:
        print(title_element) 
        print(title_element.text.strip())
        return title_element.text.strip()
    return None


    
    # Find all titles and descriptions
    # titles = soup.find_all('span', attrs={'class': 'Qwuub'}).text
    title = soup.find('span', class_='Qwuub').text.strip()
    descriptions = soup.find_all('div', attrs={'class': 'QewHA'})
    print(title)
    print(descriptions)
    # Open the CSV file for writing
    with open('tripadvisor.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Description'])
        
        # Iterate over the titles and descriptions
        for title, description in zip(title, descriptions):
            title_text = title.text.strip() if title else 'N/A'
            description_text = description.find('span', attrs={'data-test-target': 'review-text'}).text.strip() if description.find('span', attrs={'data-test-target': 'review-text'}) else 'N/A'
            writer.writerow([title_text, description_text])


