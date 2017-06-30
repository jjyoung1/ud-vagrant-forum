# "Database code" for the DB Forum.

import datetime
import psycopg2


def get_posts():
    """Return all posts from the 'database', most recent first."""

    # Setup SQL SELECT for list of posts
    req = "SELECT content, time FROM posts ORDER BY time DESC "

    # Connect to database
    db = psycopg2.connect(dbname='forum')

    # Execute request and close the connection
    c = db.cursor()
    c.execute(req)
    posts = c.fetchall()
    db.close()

    # Return posts
    return posts


def add_post(content):
    """Add a post to the 'database' with the current timestamp."""

    # Create connection
    db = psycopg2.connect(dbname='forum')

    # Setup sql insert statement
    sql = "INSERT INTO posts VALUES ('%s')" % content

    # Execute request and close the connection
    c = db.cursor()
    c.execute(sql)
    db.commit()
    db.close()
