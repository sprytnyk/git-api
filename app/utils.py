from json.decoder import JSONDecodeError

from flask import current_app
from mongoengine.queryset import Q

import requests
from requests.exceptions import ConnectionError

from app.models import Queue


def get_repositories_by_page(page=1, per_page=100):
    """
    Get repositories results from Github Search API by a number of a page.
    """

    try:
        return requests.get(
            current_app.config['GITHUB_REPOSITORY_URL'],
            params={
                'q': 'stars:>=500 language:python',
                'page': page,
                'per_page': per_page
            }
        ).json()
    except (ConnectionError, JSONDecodeError) as e:
        return {
            'message': f'{e}',
            'error': True
        }


def lock_upload():
    """
    Lock upload of repositories to DB.
    """

    queue = Queue.objects.filter(
        Q(in_progress=True) | Q(in_progress=False)
    ).first()
    if queue:
        if not queue.in_progress:
            queue.in_progress = True
            queue.save()
    else:
        queue = Queue(in_progress=True)
        queue.save()


def unlock_upload():
    """
    Unlock upload of repositories to DB.
    """

    queue = Queue.objects.filter(in_progress=True).first()
    if queue:
        queue.in_progress = False
        queue.save()


def check_lock():
    """
    Check upload lock. We'll get True, if a job has been spawned.
    """

    queue = Queue.objects.filter(in_progress=True).first()
    if queue:
        return True
    else:
        return False
