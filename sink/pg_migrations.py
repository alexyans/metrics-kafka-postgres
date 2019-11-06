#!/usr/bin/python

import psycopg2
import argparse
import os
import logging

# migration steps will be executed on deploy
up_migrations = [(
    """
    CREATE TABLE IF NOT EXISTS metrics (
        metric_id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP WITH TIME ZONE,
        metric_name VARCHAR(255),
        metric_value VARCHAR(255)       
    )
    """
)]

down_migrations = [(
    """
    DROP TABLE metrics
    """
)]

logging.basicConfig(filename="00.log", level=logging.DEBUG)


def apply_migrations(host="localhost", port=5432, db="metrics", user="admin", pwd="admin"):
    conn = None
    try:
        logging.info("%s %d %s %s %s" % (host, port, db, user, pwd))
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=pwd
        )
        
        cur = conn.cursor()

        for migration in up_migrations:
            cur.execute(migration)
        
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error("Migrations failed. \nError: %s\nExiting....")
        raise
    finally:
        if conn is not None:
            conn.close()

def rollback_db(host="localhost", port=5432, db="metrics", user="admin", pwd="admin"):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=pwd
        )
        
        cur = conn.cursor()

        for migration in down_migrations:
            cur.execute(migration)
        
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error("Migrations failed. \nError: %s\nExiting....")
        raise
    finally:
        if conn is not None:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Apply migrations to Aiven PG instance', add_help=True)
    parser.add_argument('--down', type=bool, help='Set to True to apply down migrations (default: False)', default=False)
    args = parser.parse_args()

    # get credentials from env
    host = os.environ.get('TAKEHOME_PG_HOST')
    port = int(os.environ.get('TAKEHOME_PG_PORT'))
    db = os.environ.get('TAKEHOME_PG_DATABASE')
    user = os.environ.get('TAKEHOME_PG_USER')
    pwd = os.environ.get('TAKEHOME_PG_PASSWORD')

    if args.down:
        rollback_db(host, port, db, user, pwd)
    else:
        apply_migrations(host, port, db, user, pwd)

if __name__ == "__main__":
    main()