from sanic import Sanic
from sanic.response import empty, json
from src.repo import *
from pylib.postgres import PostgresClient
from pylib.service.http import HTTPService
from pylib.proto.threads_pb2_grpc import ThreadsServiceStub
from pylib.proto.threads_pb2 import Thread, ThreadType, UpdateThreadsRequest
import grpc


class Service(HTTPService):
    def __init__(self, cfg={}):
        # Calls __init__() of the HTTPService class
        super().__init__("projects-service", cfg)

        # Sets up an insecure connection to our Threads micro-service
        channel = grpc.insecure_channel(cfg["THREADS_SVC_HOST"])
        self.threads_cli = ThreadsServiceStub(channel)

        # Connect to Postgres, sets up tables and types
        PostgresClient.connect(cfg)
        PostgresClient.migrate('up')

    def register(self):
        # Expose routes for whoever is using our API
        self.app.route('/projects/propose',
                       methods=["POST"])(self.project_propose)
        self.app.route('/projects', methods=["GET"])(self.project_list)
        self.app.route('/projects/<id:int>',
                       methods=["GET"])(self.project_details)

    async def project_list(self, req):
        """
        project_list returns a list of projects with names and taglines but no tags
        """
        pass

    async def project_details(self, req, id):
        """
        project_details returns name, tagline and tags of a project
        """
        pass

    async def project_propose(self, req):
        """
        project_propose adds a project with the given project name, tagline, tags, problems and solutions
        """
        # Adds the project name, tagline, and tags first
        project_id = update_project_details(**{k: req.json.get(k) for k in [
            "project_name", "tagline", "tags"]})

        # Adds the problems and solutions using our Threads micro-service
        self.threads_cli.UpdateThreads(UpdateThreadsRequest(
            project_id=project_id,
            threads=[Thread(
                thread_type=ThreadType.PROBLEM,
                message=p,
            ) for p in req.json.get('problems')] +
            [Thread(
                thread_type=ThreadType.SOLUTION,
                message=p,
            ) for p in req.json.get('solutions')]
        ))
        return json({
            "project_id": project_id
        })
