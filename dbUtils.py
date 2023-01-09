import psycopg2
import psycopg2.extras


def get_user(user_id, user_pw):
    cur = None
    conn = None
    try:
        conn = psycopg2.connect(host='database-1.cg318ygzj1gt.ap-northeast-2.rds.amazonaws.com', dbname='postgres', user='postgres', password='GKAMuib6FixRnXEfAxUF', port=5432)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''
        select user_nm, user_img
        from user_info
        where user_id = %s
          and user_pw = %s
        '''
        cur.execute(query, (user_id, user_pw))

        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(repr(e))
        raise e
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def upd_user_img(user_id, user_img_url):
    cur = None
    conn = None
    try:
        conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='postgres', port=5432)
        cur = conn.cursor()

        query = '''
        update user_info
        set user_img = %s
        where user_id = %s
        '''
        cur.execute(query, (user_img_url, user_id))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(repr(e))
        raise e
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    rows = get_user("test02", "qwer1234")
    print(rows)
    for row in rows:
        print(row['user_nm'])
