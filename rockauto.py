from fastapi import FastAPI
import mechanize
from bs4 import BeautifulSoup

rockauto_api = FastAPI()
BASE_URL = 'https://www.rockauto.com'
CATALOG_URL = BASE_URL + "/en/catalog/"

@rockauto_api.get("/")
async def root():
    '''Serves as a service status verication endpoint.

    Example Response:
    ```json

    {
        "message": "Rockauto Middleware API ready for requests."
    }
    ```
    '''
    return {"message": "Rockauto Middleware API ready for requests."}

@rockauto_api.get("/makes")
async def get_makes():
    '''Returns a json array of all available makes on Rockauto.

    Example Response:
    ```json
    [
        {
            "make": "ABARTH",
            "link": "https://www.rockauto.com/en/catalog/abarth"
        },
        {
            "make": "AC",
            "link": "https://www.rockauto.com/en/catalog/ac"
        },
        {
            "make": "ACURA",
            "link": "https://www.rockauto.com/en/catalog/acura"
        },
    ]
    ```
    '''

    makes_list = []

    browser = mechanize.Browser()
    page_content = browser.open(CATALOG_URL).read()

    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('div', attrs={'class', 'ranavnode'})
    soup_filter = []

    # Find US Market Only
    for x in soup:
        if 'US' in next(x.children)['value']:
            soup_filter.append( x.find('a', attrs={'class', 'navlabellink'}) )

    # Get [Make, Year, Model, Link]
    for x in soup_filter:
        makes_list.append( {'make': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })

    return makes_list

@rockauto_api.get("/years/{search_vehicle}")
async def get_years( search_make: str ):
    '''Returns a json array of years for a specified make.

    Example Response:

    ```json
    [
        {
            "make": "TOYOTA",
            "year": "2024",
            "link": "https://www.rockauto.com/en/catalog/toyota,2024"
        },
        {
            "make": "TOYOTA",
            "year": "2023",
            "link": "https://www.rockauto.com/en/catalog/toyota,2023"
        },
        ..etc
    ]

  ``
    '''

    years_list = []

    search_link = CATALOG_URL + search_make

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
        years_list.append( {'make': search_make, 'year': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })

    return years_list

@rockauto_api.get("/models/{search_vehicle}")
async def get_models( search_make: str, search_year: str):
    '''Returns a json array of model types for a specified make and year.

    Example Response:
    ```json
    [
        {
            "make": "TOYOTA",
            "year": "1995",
            "model": "4RUNNER",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,4runner"
        },
        {
            "make": "TOYOTA",
            "year": "1995",
            "model": "AVALON",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,avalon"
        },
        ...etc

    ]
    ```
    '''

    models_list = []

    search_link = CATALOG_URL + search_make + "," + search_year


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
        models_list.append( {'make': search_make, 'year': search_year, 'model': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })

    return models_list

@rockauto_api.get("/engines/{search_vehicle}")
async def get_engines(search_make: str, search_year: str, search_model: str):

    '''Returns a json array of engine types for a specified make, year and model.

    Example Return:
    ```json
    [
        {
            "make": "TOYOTA",
            "year": "1995",
            "model": "PICKUP",
            "engine": "2.4L L4",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097"
        },
        {
            "make": "TOYOTA",
            "year": "1995",
            "model": "PICKUP",
            "engine": "3.0L V6",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,3.0l+v6,1278110"
        }
    ]
    ```
    
    '''

    engines_list = []

    search_link = CATALOG_URL + search_make + "," + search_year + "," + search_model

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
        engines_list.append( {'make': search_make, 'year': search_year, 'model': search_model, 'engine': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })
    
    return engines_list

@rockauto_api.get("/categories/{search_vehicle}")
async def get_categories(search_link: str):
    '''Returns a json array of categories for a specified search link.

    Example Response:
    ```json
    [
        {
            "category": "Belt Drive",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097,belt+drive"
        },
        {
            "category": "Body & Lamp Assembly",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097,body+&+lamp+assembly"
        },
        ...etc

        ]
    ```
    '''

    categories_list = []

    browser = mechanize.Browser()
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('a', attrs={'class', 'navlabellink'})[4:]

    for x in soup:
        categories_list.append( {'category': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })

    return categories_list

@rockauto_api.get("/sub_categories/{search_vehicle}")
async def get_sub_categories(search_link: str):
    '''Returns a json array of sub categories for a specified category search link.

    Example Response:
    ```json
    [
        {
            "sub_category": "Belt",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097,belt+drive,belt,8900"
        },
        {
            "sub_category": "Idler Pulley",
            "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097,belt+drive,idler+pulley,6956"
        },
        ..etc
    ]
    ```
    '''
    
    sub_categories_list = []

    browser = mechanize.Browser()   
    page_content = browser.open( search_link).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('a', attrs={'class', 'navlabellink'})[5:]

    for x in soup:
        sub_categories_list.append( {'sub_category': x.get_text(), 'link': BASE_URL + str( x.get('href') ) })

    return sub_categories_list


@rockauto_api.get("/parts/{search_vehicle}")
async def get_parts(search_link: str):
    '''Returns a json array of part details for a specified sub-category link.
    
    Example Response:
    ```json
    [
        {
            "manufacturer": "CONTINENTAL",
            "partnumber": "49032",
            "price": "$13.58",
            "link": "https://www.rockauto.com/en/moreinfo.php?pk=1332831&cc=1278097&pt=10346"
        },
        {
            "manufacturer": "GATES",
            "partnumber": "38036",
            "price": "$15.67",
            "link": "https://www.rockauto.com/en/moreinfo.php?pk=366351&cc=1278097&pt=10346"
        },
        ...etc
    ]
    ```
    '''
    sub_categories_list = []

    browser = mechanize.Browser()   
    page_content = browser.open( search_link ).read()
    browser.close()

    soup = BeautifulSoup(page_content, features='html5lib').find_all('tbody', attrs={'class', 'listing-inner'})
    
    for s in soup:
        manufacturer = s.find('span','listing-final-manufacturer')
        partnumber = s.find('span','listing-final-partnumber')
        price = s.find('span','listing-price')
        more_info = s.find('a','ra-btn-moreinfo')
        sub_categories_list.append( {'manufacturer': manufacturer.get_text(), 'partnumber': partnumber.get_text(), 'price': price.get_text(), 'link': more_info.get('href') })

    return sub_categories_list
