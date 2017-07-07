#! /usr/bin/env python3
import psycopg2


def query_db(q):
    rows = []
    try:
        db = psycopg2.connect(dbname='news')

        c = db.cursor()
        c.execute(q)
        rows = c.fetchall()

    except Exception as e:
        print(e)

    finally:
        db.close()
        return rows


def get_popular_articles():
    # STEP 1
    # Step 1 - What are the most popular three articles of all time?
    sql = """
      SELECT title, read_count
      FROM article_reads_view
      ORDER BY read_count
      DESC LIMIT (3)
    """

    # Query the database
    rows = query_db(sql)

    print("Most Popular Articles")
    for row in rows:
        print("{} - {} views".format(row[0], row[1]))
    print('\n')


# Who are the most popular article authors of all time
def get_popular_authors():
    sql = """
      SELECT authors.name, sum(read_count) AS reads
      FROM authors JOIN article_reads_view
      ON authors.id = article_reads_view.author
      GROUP BY authors.name
      ORDER BY reads DESC;
    """

    rows = query_db(sql)

    print('Most Popular Authors')
    for row in rows:
        print("{} - {} views".format(row[0], row[1]))
    print('\n')


# Days with more than 1% errors
def get_error_statistics():
    sql = '''
      SELECT to_char(daily_errors.day, 'Mon DD, YYYY'),
          round(((daily_errors.num_errors * 100.0)/daily_requests.num_reqs),1)
          AS "Percent Errors"
      FROM daily_errors JOIN daily_requests
      ON daily_errors.day = daily_requests.day
      WHERE ((daily_errors.num_errors * 100.0)/daily_requests.num_reqs)>1.0;
      '''

    rows = query_db(sql)

    print('Days exceeding error threshold of 1%')
    for row in rows:
        print("{} - {}% errors".format(row[0], row[1]))


if __name__ == "__main__":
    get_popular_articles()
    get_popular_authors()
    get_error_statistics()
