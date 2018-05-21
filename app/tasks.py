from time import sleep

from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from app.models import Repository
from app.utils import get_repositories_by_page, lock_upload, unlock_upload
from core import celery


@celery.task()
def upload_repositories_to_mongo():
    """
    Upload data about repositories to MongoDB, if we've got already info
    about a repo, then we just update existing.
    """

    lock_upload()

    repositories = []
    # GitHub API provides us with 1000 items, so we can paginate through
    # results 10 times.
    for page in range(1, 11):
        request = get_repositories_by_page(page=page)
        if request.get('message'):
            return request['message']

        for item in request.get('items'):
            repositories.append(
                UpdateOne(
                    {
                        'full_name': item['full_name']
                    },
                    {
                        '$set': {
                            'html_url': item['html_url'],
                            'description': item['description'],
                            'stargazers_count': item['stargazers_count'],
                            'language': item['language']
                        }
                    },
                    upsert=True
                )
            )

        # Perform unordered bulk write to DB.
        try:
            Repository._get_collection().bulk_write(repositories)
        except BulkWriteError as e:
            return str(e)

    # GitHub allows us to make 10 requests per minute, so we need to take
    # a nap.
    sleep(60)

    unlock_upload()
    return 'Success'
