from fastapi import FastAPI
import mechanize
from bs4 import BeautifulSoup

rockauto_api = FastAPI()

ROCKAUTO_URL = "https://www.rockauto.com/en/catalog/"

@rockauto_api.get("/")
async def root():
    return {"message": "Hello World"}

@rockauto_api.get("/makes")
async def get_makes():
    makes_list = []

    browser = mechanize.Browser()
    page_content = browser.open('https://www.rockauto.com/en/catalog/').read()

    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('div', attrs={'class', 'ranavnode'})
    soup_filter = []

    # Find US Market Only
    for x in soup:
        if 'US' in next(x.children)['value']:
            soup_filter.append( x.find('a', attrs={'class', 'navlabellink'}) )

    # Get [Make, Year, Model, Link]
    for x in soup_filter:
        makes_list.append( {'make': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })

    return makes_list

@rockauto_api.get("/years/{search_vehicle}")
async def get_years( search_make: str ):
    years_list = []

    search_link = ROCKAUTO_URL + search_make

    browser = mechanize.Browser()
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('div', attrs={'class', 'ranavnode'})[1:]
    soup_filter = []

    # Find US Market Only
    for x in soup:
        if 'US' in next(x.children)['value']:
            soup_filter.append( x.find('a', attrs={'class', 'navlabellink'}) )

    # Get [Make, Year, Model, Link]
    for x in soup_filter:
        years_list.append( {'make': search_make, 'year': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })

    return years_list

@rockauto_api.get("/models/{search_vehicle}")
async def get_models( search_make: str, search_year: str):
    models_list = []

    search_link = ROCKAUTO_URL + search_make + "," + search_year


    browser = mechanize.Browser()
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('div', attrs={'class', 'ranavnode'})[2:]
    soup_filter = []

    # Find US Market Only
    for x in soup:
        if 'US' in next(x.children)['value']:
            soup_filter.append( x.find('a', attrs={'class', 'navlabellink'}) )

    # Get [Make, Year, Model, Link]
    for x in soup_filter:
        models_list.append( {'make': search_make, 'year': search_year, 'model': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })

    return models_list

@rockauto_api.get("/engines/{search_vehicle}")
async def get_engines(search_make: str, search_year: str, search_model: str):
    engines_list = []

    search_link = ROCKAUTO_URL + search_make + "," + search_year + "," + search_model

    browser = mechanize.Browser()
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('div', attrs={'class', 'ranavnode'})[3:]
    soup_filter = []

    # # Find US Market Only
    for x in soup:
            soup_filter.append( x.find('a', attrs={'class', 'navlabellink'}) )

    # Get [Make, Year, Model, Link]
    for x in soup_filter:
        engines_list.append( {'make': search_make, 'year': search_year, 'model': search_model, 'engine': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })
    
    return engines_list

@rockauto_api.get("/categories/{search_vehicle}")
async def get_categories(search_link: str):
    categories_list = []

    browser = mechanize.Browser()
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('a', attrs={'class', 'navlabellink'})[4:]

    for x in soup:
        categories_list.append( {'category': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })

    return categories_list

@rockauto_api.get("/sub_categories/{search_vehicle}")
async def get_sub_categories(search_link: str, category: str):
    sub_categories_list = []

    browser = mechanize.Browser()   
    page_content = browser.open( search_link + "," + category ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('a', attrs={'class', 'navlabellink'})[5:]

    for x in soup:
        sub_categories_list.append( {'sub_category': x.get_text(), 'link': 'https://www.rockauto.com' + str( x.get('href') ) })

    return sub_categories_list
