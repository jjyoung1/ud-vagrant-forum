import psycopg2

# Views
# """-- Create view for number article views from logs
# CREATE VIEW article_reads_view AS
#   SELECT title, author, count(*) AS read_count
#   FROM log JOIN articles ON log.path  LIKE '%' || articles.slug || '%'
#   WHERE path != '/'
#   GROUP BY author, title;
#
# -- Total number of requests per day
# CREATE VIEW daily_requests AS
# SELECT date_trunc('day', time) as day, count(*) as num_reqs
#   FROM log
#   GROUP BY day;
#
# -- Total number of errors per day
# CREATE VIEW daily_errors AS
# SELECT status, date_trunc('day', time) as day, count(*) as num_errors
#   FROM log
#   WHERE status LIKE '4%'
#   GROUP BY day, status;
# """

# Step 2 - Who are the most popular article author of all time
most_popular_authors_sql = """
  SELECT authors.name, sum(read_count) as reads
  FROM authors JOIN article_reads_view ON authors.id = article_reads_view.author
  GROUP BY authors.name
  ORDER BY reads DESC;
"""

db = psycopg2.connect(dbname='news')

# STEP 1
# Step 1 - What are the most popular three articles of all time?
most_popular_articles_sql = """ 
  SELECT title, count(*) AS likes
  FROM articles JOIN log ON log.path LIKE CONCAT('%', articles.slug)  
  WHERE path != '/' 
  GROUP BY title 
  ORDER BY likes 
  DESC LIMIT (3)
"""

c = db.cursor()
c.execute(most_popular_articles_sql)
rows = c.fetchall()

print("Most Popular Articles")
for row in rows:
    print("{} - {} views".format(row[0], row[1]))
print('\n')

# STEP 2
c = db.cursor()
c.execute(most_popular_authors_sql)
rows = c.fetchall()

print('Most Popular Authors')
for row in rows:
    print("{} - {} views".format(row[0], row[1]))
print('\n')

# -- Step 3: Days with more than 1% errors
days_over_error_threshold = '''
  SELECT to_char(daily_errors.day, 'Mon DD, YYYY'),
      trunc(((daily_errors.num_errors * 100.0)/daily_requests.num_reqs),1) AS "Percent Errors"
  FROM daily_errors JOIN daily_requests
  ON daily_errors.day = daily_requests.day
  WHERE ((daily_errors.num_errors * 100.0)/daily_requests.num_reqs)>1.0;
  '''

c = db.cursor()
c.execute(days_over_error_threshold)
rows = c.fetchall()

print('Days exceeding error threshold of 1%')
for row in rows:
    print("{} - {}% errors".format(row[0], row[1]))

db.close()