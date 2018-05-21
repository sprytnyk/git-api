from json import loads

from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.models import Repository
from app.tasks import upload_repositories_to_mongo
from app.utils import check_lock


class UploadRepositoriesResource(Resource):
    """
    This resource search for python repositories with >=500 stars on GitHub
    and upload it to MongoDB.
    """

    def get(self):
        if check_lock():
            return {
                'message': 'We are already working on repositories.',
                'error': False
            }
        else:
            upload_repositories_to_mongo.delay()

            return {
                'message': 'The job created.',
                'error': False
            }


class RepositoriesResource(Resource):
    """
    Show repositories, that available in our DB.
    """

    def get(self):
        args = self.create_parser().parse_args()
        repositories = Repository.objects.all()
        if args['sort_by_stars']:
            repositories = repositories.order_by('-stargazers_count')
        else:
            repositories = repositories.order_by('stargazers_count')

        return repositories.paginate(
            args['page'],
            current_app.config['ITEMS_PER_PAGE']
        ).items

    @staticmethod
    def create_parser():
        """
        Parse request args.
        """

        parser = RequestParser()
        parser.add_argument(
            'sort_by_stars', type=lambda x: loads(x), default=False
        )
        parser.add_argument('page', type=int, default=1)

        return parser
