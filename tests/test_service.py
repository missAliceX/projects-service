import mock
import asyncio
from src import service
from tests import ServiceTestCase
from pylib.proto.threads_pb2_grpc import ThreadsServiceStub
from pylib.proto.threads_pb2 import Thread, ThreadType, UpdateThreadsRequest


class TestProjectsService(ServiceTestCase):
    @mock.patch("src.service.PostgresClient.connect")
    @mock.patch("src.service.PostgresClient.migrate")
    def test_new_service(self, migrate, connect):
        # Creates a new service
        svc = service.Service(self.test_cfg)

        # Ensures we are connected to the Threads micro-service
        self.assertIsInstance(svc.threads_cli, ThreadsServiceStub)

        # Ensures that Postgres is connected and migratiing properly
        connect.assert_called_with(self.test_cfg)
        migrate.assert_called_with('up')

    @mock.patch("pylib.service.http.Sanic")
    def test_register(self, Sanic):
        # Mock Sanic HTTP server so we do not actually start running the server
        Sanic.return_value = mock.MagicMock()

        # Creates a new service
        svc = service.Service(self.test_cfg)

        # Ensure that we added routes
        svc.app.route.assert_called()

    @mock.patch("pylib.service.http.Sanic")
    @mock.patch("src.service.update_project_details")
    def test_project_propose(self, update_project_details, Sanic):
        # Mock Sanic HTTP server so we do not actually start running the server
        Sanic.return_value = mock.MagicMock()

        # Creates a new service
        svc = service.Service(self.test_cfg)

        # Mock the Threads micro-service so we don't actually make a call to the micro-service
        svc.threads_cli = mock.MagicMock()
        update_project_details.return_value = 3
        req = mock.MagicMock()
        req.json = {
            "project_name": "test-project",
            "tagline": "this is a test project",
            "tags": ["happy", "sad"],
            "problems": ["this is a problem", "not a problem"],
            "solutions": ["modern problems requires modern solutions"],
        }

        # Run project_propose() and ensure the appropriate data is sent to the micro-service
        asyncio.run(svc.project_propose(req))
        svc.threads_cli.UpdateThreads.assert_called_with(UpdateThreadsRequest(
            project_id=3,
            threads=[
                Thread(thread_type=ThreadType.PROBLEM, message=req.json['problems'][0]),
                Thread(thread_type=ThreadType.PROBLEM, message=req.json['problems'][1]),
                Thread(thread_type=ThreadType.SOLUTION, message=req.json['solutions'][0]),
            ]
        ))

    @mock.patch("pylib.service.http.Sanic")
    @mock.patch("src.service.update_project_details")
    def test_project_propose_error(self, update_project_details, Sanic):
        # Mock Sanic HTTP server so we do not actually start running the server
        Sanic.return_value = mock.MagicMock()

        # Creates a new service
        svc = service.Service(self.test_cfg)

        # Mock the Threads micro-service so we don't actually make a call to the micro-service
        svc.threads_cli = mock.MagicMock()
        update_project_details.side_effect = Exception("test")
        req = mock.MagicMock()
        req.json = {}

        # Ensure that running project_propose() raises an exception and that the micro-service is not called
        self.assertRaises(Exception, asyncio.run, svc.project_propose(req))
        svc.threads_cli.UpdateThreads.assert_not_called()