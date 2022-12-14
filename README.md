# REST API for spatial data

This is a multi-part project containing following services:



![Untitled Diagram drawio](https://user-images.githubusercontent.com/63467008/185849123-ad1aefe8-16d4-4d45-b62e-36d152d49a7d.png)



#### 1. Geodjango
  - Connected to postgresql via postgis
  - Populate postgresql database with the geojson present at https://datahub.io/core/geo-countries#resource-geo-countries_zip
  - Accomodate CRUD operations as an entrypoint to the database to fetch and manipulate
  - Query the database spatially and non-spatially

#### 2. Main
  - Downloads geojson at https://datahub.io/core/geo-countries#resource-geo-countries_zip to periodically update it with any dataset changes
  
#### 3. Pub-sub mechanism
  - Geodjango and Main modules communicate throgh pub-sub mechanism using RabbitMQ
  - Main enqueues any changes noticed in the dataset every 10 minutes
  - Geodjango module listens to the queue and updates the changes in the database
  
#### 4. Nginx
  - Nginx acts as the loadbalancer. 2 instances of the 'api' app is created on ports 8000 and 8005. Nginx re-routes the requests to the 2 ports running on the same server (can be changed to apps running on different servers). In case, if an instance is down, the other server serves the requests.
  
## RUN THE APPLICATION
- Clone the repository
- Open a Terminal and enter 'geodjango' directory using: 
  - ```cd geodjango```
- Run docker compose command: 
  - ```docker-compose up```

- Open another terminal and enter 'main' directory using: 
  - ```cd main```
- Run docker compose command: 
  - ```docker-compose up```

## WORK AROUND WITH THE APPLICATION
- Open the browser
- To populate the database for the very first time, hit http://localhost:8005/api/countries with the put request (not standardized method)
    - ```PUT http://localhost:8005/api/countries```
- To fetch the complete database:
    - ```GET http://localhost:8005/api/countries```
- Fetch specific country using id
    - ```GET http://localhost:8005/api/countries/<str:id>```
- Create:
    - ```POST http://localhost:8005/api/countries```
      - Sample body:
    ```
    {
    "admin": "India",
    "iso_a3": "test_iso_a3",
    "geometry_type": "MultiPolygon",
    "coordinates": "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))"
    }
    ```
- Update specific country using id
    - ```PUT http://localhost:8005/api/countries/<str:id>```
      - Sample body:
    ```
    {
    "admin": "India",
    "iso_a3": "test_iso_a3_changed",
    "geometry_type": "MultiPolygon",
    "coordinates": "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))"
    }
    ```
- Delete specific country using id
    - ```DELETE http://localhost:8005/api/countries/<str:id>```
- Non-spatial querying; fetch countries by name:
    - ```GET http://localhost:8005/api/countries/name/<str:name>```
- Spatial query; fetch all countring intersecting with a specific country:
    - ```GET http://localhost:8005/api/countries/intersect/<str:name>```
- Note: Any changes in the database are being monitored in the background and updated
![Capture](https://user-images.githubusercontent.com/63467008/185846198-13a2f575-780b-42ac-bee0-771e06afbfb0.PNG)
