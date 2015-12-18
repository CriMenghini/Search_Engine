# Collect library
# Author: Cristina Menghini 

import requests
import time
import os
from bs4 import BeautifulSoup
import codecs
import shutil

def CreateDIR(path):
# This function creates the directory Documents.
#- path is a string and corresponds to the path of the directory Documents.
    try: #create the directory /Documents
        os.makedirs(path+'/Documents')
    except OSError:
        if not os.path.isdir(path+'/Documents'):
            raise
    return path+'/Documents'

def ListWebSite(doc_website):
#Create the list of the baseURL of all the web pages I'm interested in. 
#- doc_website: the file in which the links are saved.
    list_site = [line for line in open(doc_website, 'r+')]
    sites = []
    for i in range(len(list_site)):
        sites.append(list_site[i].rstrip())
    return sites

def Kijiji (website, page, dirsize, directory ,delay=2):
# This function returns the text of each ad in one page and save it in a document in /Documents directory.
#- website is the BASEurl of the page we want to download(ListWebSite[0]);
#- page is the page of the website I want to download;
#- dirsize corresponds to the number of elements that /Documents contains;
#- directory is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each ads
    r = requests.get( website + str(page))
    html = r.content
    soup = BeautifulSoup(html) # download the html of the page
    links = soup.find_all('a', 'cta') # extract the links of each ad in the page
    k = 1 # counter
    for item in links:
        title = item.h3.string.encode('utf-8').translate(None,'\t').strip()
        location = item.find(class_ = 'locale').string.encode('utf-8').translate(None,'\t').strip()
        price = item.find(class_ = 'price').string.encode('utf-8').translate(None,'\t').strip()
        url = item.get('href')
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html)
        extra = soup.find_all(class_ = 'ad-data')
        for item in extra:
            description = item.find(class_ = 'ki-view-ad-description').string.encode('utf-8').translate(None,'\t').strip()
            infs = item.find_all('div', class_ = ['key','value'])
            informs = []
            for i in range(len(infs)): # extract the extra informations for each ad
                informs.append(infs[i].get_text().encode('utf-8').translate(None,'\n\r\t').strip())
                extra_inf = [' - '.join([informs[i],informs[i+1]]) for i in range(0,len(informs)/2,2)]
                extra_info = '\t'.join(extra_inf[:])
        text = '%s\t %s\t %s\t %s\t %s\t %s\t ' % (title,location,price,url,description,extra_info) 
        with open(os.path.join(directory,'documents-'+str(0)*(6-len(str(dirsize+k)))+str(dirsize+k)), 'w' )  as f:
            f.write(text)  
        time.sleep(delay)
        k += 1 


def AllKijiji( min_pag, max_pag, website, DIR,delay = 2):
# This function downloads and stores all the ads that are in the selected pages.
#- min_pag is the lower endpoint of the interval of pages I want to download;
#- max_pag is the greater endpoint of the interval of pages I'm interesting in;
#- website is the BASEurl of Kijiji( ListWebSite('Sites.txt')[0]
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each page.
    for j in range(min_pag,max_pag+1):
        sizeDIR = len(os.listdir(DIR))
        Kijiji( website , j, sizeDIR, DIR)
        time.sleep(delay)

def Immobiliare (website, page, DIR, delay = 2):
# This function returns the text of each ad in one page.
#- website is the BASEurl of the page we want to download(ListWebSite[1]);
#- page is the page of the website I want to download;
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each ads.
    r = requests.get(website + str(page))
    html = r.content
    soup = BeautifulSoup(html) # download the html of the page
    links = soup.find_all('div', 'annuncio_title') # extract the links of each ad in the page
    for item in links:
        url = item.a['href']
        if 'http://www.immobiliare.it' in url:
            r = requests.get(url)
            html = r.content
            soup = BeautifulSoup(html)
            title = soup.find('strong',class_ = 'h3' ).get_text().encode('utf-8').translate(None,'\t').strip()
            locs = soup.find_all('div', style="float:left;margin:10px 0 0 0")
            for item in locs:
                locations = item.find('div').string.encode('utf-8').translate(None,'\t').strip()
            price = soup.find('strong',style = 'font-size:14px;').string.encode('utf-8').translate(None,'\t').strip()
            description = soup.find('div',class_ = 'descrizione').get_text().encode('utf-8').translate(None,'\t').strip()
            infos = soup.find_all('tr')
            informs = []
            for j in range(3,14): # extract the extra informations for each ad
                infs = infos[j].find_all('td')
                for i in range(len(infs)):
                    informs.append(infs[i].get_text().encode('utf-8').translate(None,'\t').strip())
                    extra_inf = [' '.join([informs[i],informs[i+1]]) for i in range(0,len(informs)/2,2)]
                    extra_info = '\t'.join(extra_inf[:])
            len_dir = len(os.listdir(DIR))
            text = '%s\t %s\t %s\t %s\t %s\t %s\t ' % (title,locations,price,url,description,extra_info)
            with open(os.path.join(DIR,'documents-'+str(0)*(6-len(str(len_dir+1)))+str(len_dir+1)), 'w' )  as f:
                f.write(text)  
        time.sleep(delay)

def AllImmobiliare(min_pag, max_pag, website, DIR, delay=2):
# This function downloads and stores all the ads that are in the selected pages.
#- min_pag is the lower endpoint of the interval of pages I want to download;
#- max_pag is the greater endpoint of the interval of pages I'm interesting in;
#- website is the BASEurl of Immobiliare( ListWebSite('Sites.txt')[0]
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each page.
    for j in range(min_pag, max_pag+1):
        Immobiliare(website,j, DIR)
        time.sleep(delay)

def Attico (page,website, DIR, delay = 2):
# This function returns the text of each ad in one page.
#- website is the BASEurl of the page we want to download(ListWebSite[2]);
#- page is the page of the website I want to download;
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each ads.
    r = requests.get(website + str(page))
    html = r.content
    soup = BeautifulSoup(html) # download the html of the page
    links = soup.find_all('div', class_ = 'snippet-center') # extract the links of each ad in the page
    for item in links:
        url = item.a['href']
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html)
        title = soup.find('h1', 'fn').contents[0].encode('utf-8').translate(None,'\t').strip()
        location = soup.find('h1', 'fn').contents[1].get_text().encode('utf-8').translate(None,'\t').strip()
        price = soup.find('span', class_ = 'ad-box-price').get_text().encode('utf-8').translate(None,'\t').strip()
        description = soup.find('div','ad-description description').get_text().encode('utf-8').translate(None,'\t').strip()
        infos = soup.find_all('div', class_ = 'ad-details')
        informs = []
        infs = infos[0].find_all('li') # extract the extra informations for each ad
        for i in range(len(infs)):
            informs.append(infs[i].get_text().encode('utf-8').translate(None,'\n\r\t').strip())
        extra_info = '\t'.join(informs[:])
        len_dir = len(os.listdir(DIR))
        text = '%s\t %s\t %s\t %s\t %s\t %s\t ' % (title, location,price, url, description, extra_info)
        with open(os.path.join(DIR,'documents-'+str(0)*(6-len(str(len_dir+1)))+str(len_dir+1)), 'w' )  as f:
            f.write(text)
        time.sleep(delay)

def AllAttico(min_pag, max_pag, webpage, DIR,delay=2):
# This function downloads and stores all the ads that are in the selected pages.
#- min_pag is the lower endpoint of the interval of pages I want to download;
#- max_pag is the greater endpoint of the interval of pages I'm interesting in;
#- webpage is the BASEurl of Attico( ListWebSite('Sites.txt')[2])
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- delay is the time between the download of each page.
    for j in range(min_pag, max_pag+1):
        Attico(j, webpage, DIR )
        time.sleep(delay)

def CreateAllDocs(sitedoc, DIR, minKijiji, maxKijiji, minImm, maxImm, minAtt, maxAtt):
# This function creates the collection of the search engine.
#- sitedoc is the name of the file that containes the list of websites from which I extract the ads( string);
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is);
#- minKijiji is the lower endpoint of the interval of pages I download from Kijiji;
#- maxKijiji is the upper endpoint of the interval of pages I download from Kijiji;
#- minImm is the lower endpoint of the interval of pages I download from Immobiliare;
#- maxImm is the upper endpoint of the interval of pages I download from Immobiliare;
#- minAtt is the lower endpoint of the interval of pages I download from Attico;
#- maxAtt is the upper endpoint of the interval of pages I download from Attico.
    for i in range(len(ListWebSite(sitedoc))):
        if i == 0:
            AllKijiji(minKijiji, maxKijiji,ListWebSite(sitedoc)[0], DIR)
        if i == 1:
            AllImmobiliare(minImm,maxImm,ListWebSite(sitedoc)[1], DIR)
        if i == 2:
            AllAttico(minAtt,maxAtt, ListWebSite(sitedoc)[2], DIR)  

def Subdirs(dim_sub, DIR):
# This function creates the subfolders and stores put in it all the documents contained in /Documents.
#- dim_sub is the dimention of the subdirs I generate;
#- DIR is /Document and it's simply the return of CreateDir(path of the directory in which /Documents is).
    num_fol = len(os.listdir(DIR))/dim_sub
    if len(os.listdir(DIR))%dim_sub == 0:
        num_fol = len(os.listdir(DIR))/dim_sub
    else: num_fol =  len(os.listdir(DIR))/dim_sub + 1
    for i in range(0,num_fol):
        endpoint_min = (dim_sub*i)+1 
        if (len(os.listdir(DIR))-i) < dim_sub:
            endpoint_max =endpoint_min + (len(os.listdir(DIR))-i) - 1
        else: 
            endpoint_max = endpoint_min+(dim_sub-1)
        name_fol = 'documents-'+'0'*(6-len(str(endpoint_min)))+str(endpoint_min)+'-'+'0'*(6-len(str(endpoint_max)))+str(endpoint_max)
        try:
            os.makedirs(DIR+'/'+name_fol)
        except OSError:
            if not os.path.isdir(DIR+'/'+name_fol):
                raise
        for j in range(endpoint_min, (endpoint_max+1)):
            shutil.move(DIR+'/documents-'+str(0)*(6-len(str(j)))+str(j), DIR+'/'+name_fol)    
