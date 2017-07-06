# Log Analysis Project

Requirements:
1. Udacity VM installed
2. 'news' database prepopulated
3. psycopg2 library installed

##SQL Views:
-- Create view for number article views from logs
CREATE VIEW article_reads_view AS
  SELECT title, author, count(*) AS read_count
  FROM log JOIN articles ON log.path  LIKE '%' || articles.slug || '%'
  WHERE path != '/'
  GROUP BY author, title;

-- Total number of requests per day
CREATE VIEW daily_requests AS
SELECT date_trunc('day', time) as day, count(*) as num_reqs
  FROM log
  GROUP BY day;

-- Total number of errors per day
CREATE VIEW daily_errors AS
SELECT status, date_trunc('day', time) as day, count(*) as num_errors
  FROM log
  WHERE status LIKE '4%'
  GROUP BY day, status;

##To Execute:
1. Unpack zip file into a directory
2. cd into directory containing analyze.py file
3. run 'python3 analyze.py'

##Expected output for prepopulated database:
See file sampleout.txt