# A simple and easy to use Rockauto FastAPI middleware

This API serves as a middleware between Rockauto and other applications. It uses web scrapping to gather data from Rockauto and returns it in a nice JSON format.


# Usage

1. Install the required python packages using `pip install -r requirements.txt`
2. Start the FastAPI server using the command `fastapi dev rockauto.py`
3. Navigate to the swagger docs and try it out: http://127.0.0.1:8000/docs

# Examples usage

For this example, we skip the makes, years, and models endpoints. These (along with `/engines`) can be assembled easily because they do not require any unique ids:
```python

search_make = "TOYOTA"
search_year = "1995"
search_model = "PICKUP"
search_link = "https://www.rockauto.com/en/catalog/" + search_make + "," + search_year + "," + search_model

```
After making a request to `/engines` below, it will return a link that will have a unique ID on the end of it. It is unknown what this actually is, but I assume it is an internal reference ID of some kind for the categories and it's used in an effort to prevent webscraping (lolz pwn'd xD)

### Request to `/engines`:
Curl
```bash 
curl -X 'GET' \
  'http://127.0.0.1:8000/engines/{search_vehicle}?search_make=TOYOTA&search_year=1995&search_model=PICKUP' \
  -H 'accept: application/json'
```
Response
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
### From the above, you can use the "link" of the engine type to make a request to `/categories`:
Curl
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/categories/{search_vehicle}?search_link=https%3A%2F%2Fwww.rockauto.com%2Fen%2Fcatalog%2Ftoyota%2C1995%2Cpickup%2C2.4l%2Bl4%2C1278097' \
  -H 'accept: application/json'

  ```
Response
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
### You can then make a request to `sub_categories/` using the link provided in the category response:
Curl
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/sub_categories/{search_vehicle}?search_link=https%3A%2F%2Fwww.rockauto.com%2Fen%2Fcatalog%2Ftoyota%2C1995%2Cpickup%2C2.4l%2Bl4%2C1278097%2Cbelt%2Bdrive' \
  -H 'accept: application/json'
```
Response
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
  {
    "sub_category": "Tensioner Pulley",
    "link": "https://www.rockauto.com/en/catalog/toyota,1995,pickup,2.4l+l4,1278097,belt+drive,tensioner+pulley,10346"
  }
]
```


### Finally, you can make a request to `/parts` using the link provided in the sub category response.
Curl
```bash 
curl -X 'GET' \
  'http://127.0.0.1:8000/parts/{search_vehicle}?search_link=https%3A%2F%2Fwww.rockauto.com%2Fen%2Fcatalog%2Ftoyota%2C1995%2Cpickup%2C2.4l%2Bl4%2C1278097%2Cbelt%2Bdrive%2Ctensioner%2Bpulley%2C10346' \
  -H 'accept: application/json'
```
Response
```json
[
  {
    "manufacturer": "CONTINENTAL",
    "partnumber": "49032",
    "price": "$13.58",
    "more_info": "https://www.rockauto.com/en/moreinfo.php?pk=1332831&cc=1278097&pt=10346"
  },
  {
    "manufacturer": "GATES",
    "partnumber": "38036",
    "price": "$15.67",
    "more_info": "https://www.rockauto.com/en/moreinfo.php?pk=366351&cc=1278097&pt=10346"
  },
  {
    "manufacturer": "ACDELCO",
    "partnumber": "38036",
    "price": "$22.79",
    "more_info": "https://www.rockauto.com/en/moreinfo.php?pk=506481&cc=1278097&pt=10346"
  },
  {
    "manufacturer": "ULTRA-POWER",
    "partnumber": "38036",
    "price": "Out of Stock",
    "more_info": "https://www.rockauto.com/en/moreinfo.php?pk=8498176&cc=1278097&pt=10346"
  }
]
```



# Docker 
Coming soon!
