"""
@author: Somesh Herath Bandara (sgherath)
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
from itertools import islice

deleted_rows = []
new_rows = []

def go_to_first_result(search_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    html_soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        movie_page = html_soup.find('td', 'result_text').find('a').get('href')
    except:
        movie_page = ""

    return movie_page

def scrape(movie_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(movie_page_url, headers=headers)
    html_soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        main_director = html_soup.findAll('div', {'class': 'credit_summary_item'})[0].find('a').get_text()
    except:
        main_director = ""

    try:
        main_writer = html_soup.findAll('div', {'class': 'credit_summary_item'})[1].find('a').get_text()
    except:
        main_writer = ""
    try:
        main_actor = html_soup.findAll('div', {'class': 'credit_summary_item'})[2].find('a').get_text()
    except:
        main_actor = ""
    
    try:
        genre = html_soup.findAll('div', {'class': 'see-more inline canwrap'})[1].find('a').get_text()
    except:
        genre = ""

    try:
        year = html_soup.find('span', {'id': 'titleYear'}).find('a').get_text()
    except:
        year = ""

    movie_data =[main_director, main_writer, main_actor, genre, year]

    return movie_data

def slicer(reader, writer, count):
    for row in islice(reader,  count, None):
        try:
            search_url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + '+'.join([row[2]]) + '&s=all'
            movie_page_url = go_to_first_result(search_url)
            movie_page = urljoin(search_url, movie_page_url)
            if(movie_page == ""):
                deleted_rows.append(row[0])
                continue
            movie_data = scrape(movie_page)
        
            if(movie_data[0] == "" or  movie_data[1] == "" or movie_data[2] == "" or movie_data[3] == ""):
                deleted_rows.append(row[0])
                continue
        
            if(row[1] != movie_data[4]):
                deleted_rows.append(row[0])
                #print(row[1]+" "+movie_data[4]+"ss\n")
                continue

            new_row = [row[0], row[1], row[2], movie_data[0], movie_data[1], movie_data[2], movie_data[3]]
            #print(new_row)
            #new_rows.append(new_row)
            writer.writerow(new_row)
        except:
            deleted_rows.append(row[0])
            continue
        
def manual_slicer(reader,count, start):
    while True:
            row = next(reader)
            if(row[0] == start):
                print(row[0])
                break


with open('movie_titles.csv') as csvfile_read, open('new_movie_data.csv', 'a') as csvfile_write:
    reader = csv.reader(csvfile_read, delimiter=',')
    writer = csv.writer(csvfile_write)
    
    count = 0

    #put where you want to start here. if you stopped at 6391 (where the utf error was), put that.
    manual_slicer(reader,count, "6391")

    while True:
        try:
            row = next(reader)
            count +=1
        except UnicodeDecodeError:
            count +=1
            continue
        except StopIteration:
            break
        
        try:
            search_url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + '+'.join([row[2]]) + '&s=all'
            movie_page_url = go_to_first_result(search_url)
            movie_page = urljoin(search_url, movie_page_url)
            if(movie_page == ""):
                deleted_rows.append(row[0])
                continue
            movie_data = scrape(movie_page)
        
            if(movie_data[0] == "" or  movie_data[1] == "" or movie_data[2] == "" or movie_data[3] == ""):
                deleted_rows.append(row[0])
                continue
        
            if(row[1] != movie_data[4]):
                deleted_rows.append(row[0])
                #print(row[1]+" "+movie_data[4]+"ss\n")
                continue

            new_row = [row[0], row[1], row[2], movie_data[0], movie_data[1], movie_data[2], movie_data[3]]
            print(new_row)
            #new_rows.append(new_row)
            writer.writerow(new_row)
            csvfile_write.flush()
        except:
            deleted_rows.append(row[0])
            continue

csvfile_write.close()
csvfile_read.close()







