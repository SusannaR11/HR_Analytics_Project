from utilities.read_DB import AdsDB

# init db connection
db = AdsDB()

    # query function for occupation 
    # ensure field=Data/IT b4 run
def occupation_query():
             
                df_occupation = db.query("""
                        SELECT occupation as beteckning, 
                        sum(vacancies) AS antal
                        FROM marts.mart_data_it
                        GROUP BY occupation
                        ORDER BY antal DESC""")
                
                pie_occupation_grouped(df_occupation)
                db.close()