import os
import psycopg2
import urlparse


def config():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse('postgres://wmmfkosp:ZkVyvu18H58EuM-5ti38OAnE-mlRKtKS@salt.db.elephantsql.com:5432/wmmfkosp')
    # print('url.path[1:]: ', url.path[1:])
    conn = psycopg2.connect(database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn
    
def connect(pg_query):
    """ Connect to the PostgreSQL database server """
    # print('def connect en postgres_db')
    # conn = None
    try:
        # read connection parameters
        # params = config()
        conn = config()
        # print('params: ', params)
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        # conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(host=hostname,user=username, password=password, dbname=database)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('pg_query: ', pg_query)
        cur.execute(pg_query)
        # cur.query(pg_query)
    
        # display the PostgreSQL database server version
        rows = cur.fetchall()
        print('rows: ', rows)
        # close the communication with the PostgreSQL
        cur.close()

        return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error de coneccion: ', error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

