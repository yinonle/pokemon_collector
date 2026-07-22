from DB.data_base import engine

def test_db_connection():
    try: 
        with engine.connect() as connection:
            print("Connection success")
            
    except Exception as e:
        print("Connection faild")
        print(e)

if __name__ == "__main__":
    test_db_connection()