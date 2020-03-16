# Kickstart
To bootstrap project, just run docker-compose inside root directory with docker-compose.yml. E.g.:
```sh
docker-compose up
```
Then go to http://localhost:5005 to be able to see what's going out.
Endpoints list:

| Method | Endpoint | URL params | Description |
| ------ | ------ | ------ | ------ |
| GET | /api/v1/upload-repositories/ | - | Upload repositories from Github Search API to our DB. |
| GET | /api/v1/repositories/ | `page` (int), `sort_by_stars` (bool) | Fetch repositories from our DB. |
