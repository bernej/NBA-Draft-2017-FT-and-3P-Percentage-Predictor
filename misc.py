# Helper Module with miscellaneous functionality


# Gathers all the season stat lines and returns them in dictionaries
def query_tables(db):

    # Gather the Top prospects
    cur = db.cursor()
    cur.execute('SELECT * FROM prosp_per40')
    prosp_per40_results = cur.fetchall()

    # Gather all the NBA comps (per 40 minutes stats)
    cur = db.cursor()
    cur.execute('SELECT * FROM comps_per40')
    comps_per40_results = cur.fetchall()


    # Return the dictionaries with all the season stat lines
    return prosp_per40_results, comps_per40_results