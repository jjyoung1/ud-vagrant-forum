# Log Analysis Project

## Required Software:
* [Vagrant](https://www.vagrantup.com/downloads.html) installed
* Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed

## Execution environment
* Get Udacity VM configuration from [GitHub](https://github.com/udacity/fullstack-nanodegree-vm)
* Change directory into **/vagrant**
* Download database initialization code from 
  **[here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)**
* Populate the **news** database using **psql -d news -f newsdata.sql**
  
* psycopg2 library installed using **pip install psycopg2** or otherwise as desired


## SQL Views:
### View for number articles from logs
CREATE VIEW article_reads_view AS<br />
  SELECT title, author, count(*) AS read_count<br />
  FROM log JOIN articles ON log.path<br />
  LIKE '%' || articles.slug || '%'<br />
  WHERE path != '/' AND log.status = '200 OK'<br />
  GROUP BY author, title;<br />

### Total number of requests per day
CREATE VIEW daily_requests AS<br />
SELECT date_trunc('day', time) as day, count(*) as num_reqs<br />
  FROM log<br />
  GROUP BY day;<br />

### Total number of errors per day
CREATE VIEW daily_errors AS<br />
SELECT status, date_trunc('day', time) as day, count(*) as num_errors<br />
  FROM log<br />
  WHERE status LIKE '4%'<br />
  GROUP BY day, status;<br />

## To Execute:
1. Unpack zip file into a directory
2. cd into directory containing analyze.py file
3. run 'python3 analyze.py'

## Expected output for prepopulated database:
See file sampleout.txt