import psycopg2
from src import repo
from pylib.testutil import postgres
from tests import ServiceTestCase


class TestProjectsRepo(ServiceTestCase):
    def test_update_project_details(self):
        # Call update_project_details() to add a project with the respective details
        project_id = repo.update_project_details("test", "I am a decent test", ["testing", "coverage"])
        self.assertEqual(project_id, 1)

        # Retrieve projects and tags data
        with postgres.repo() as cursor:
            cursor.execute("select * from projects")
            projects = cursor.fetchall()
            cursor.execute("select * from tags")
            tags = cursor.fetchall()

        # Ensure that the data added is what we expect
        self.assertEqual(projects, [(1, 'test', 'I am a decent test')])
        self.assertEqual(tags, [(1, 1, 'testing'), (2, 1, 'coverage')])

    def test_update_project_details_error(self):
        # Ensure that update_project_details() raises an exception when we have a None value for tags
        self.assertRaises(psycopg2.errors.NotNullViolation, repo.update_project_details, "test", "I am a decent test", [None])

        # Check that projects and tags are NOT added to the database
        with postgres.repo() as cursor:
            cursor.execute("select * from projects")
            projects = cursor.fetchall()
            cursor.execute("select * from tags")
            tags = cursor.fetchall()
        self.assertEqual(projects, [])
        self.assertEqual(tags, [])