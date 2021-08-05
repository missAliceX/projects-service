from pylib.postgres import PostgresClient


def get_projects_listing(limit: int = 50):
    """
    get_projects_listing retrieves up to "limit" number of project names and taglines ordered by date.
    """
    pass


def get_project_details(project_id: int):
    """
    get_project_details retrieves not only the project name and tagline, but also all of its tags.
    """
    pass


def update_project_details(project_name, tagline, tags):
    """
    update_project_details adds a project provided its name, tagline and tags
    """
    with PostgresClient.repo() as cursor:
        cursor.execute(
            "insert into projects(project_name, tagline) values (%s, %s) RETURNING project_id",
            [project_name, tagline])
        project_id = cursor.fetchone()[0]
        cursor.execute(
            f"insert into tags(project_id, tag) values {','.join(['%s'] * len(tags))}",
            [(project_id, t) for t in tags]
        )
        return project_id
