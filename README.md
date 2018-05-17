# Fork this project and send back a pull request.

## What to do
Create a simple RESTful API that imports data from GitHub Search API https://developer.github.com/v3/search/

Import repositories that have been written in Python and have more than 500 stars. Import just a few fields from GitHub Search API:
 `full_name`, `html_url`, `description`, `stargazers_count`, `language`.
 
You may use any database or just store repositories in a RAM.

REQUIREMENTS:
1. It is necessary to do a script/function/endpoint to fill the database.
2. Add pagination to API.
3. Add docsrings and comments to your code.
4. Describe your solution in the README.md file.

## Bonus 1
Add sorting by `stars` to an API.

## Bonus 2
Use docker compose encapsulating all the services related to this app.

## Some help
* How to fork https://confluence.atlassian.com/bitbucket/forking-a-repository-221449527.html
* How to create a pull request https://confluence.atlassian.com/bitbucket/create-a-pull-request-774243413.html