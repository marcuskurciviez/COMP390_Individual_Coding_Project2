import requests
import json
import sqlite3


def convert_content_to_json(response: requests.Response):
    json_data_obj = None
    if response is None:
        print(f'JSON Decode not executed: No response object! \n')
        return None
    try:
        json_data_obj = response()
        print(f'Response object content converted to JSON object. \n')
        return None
    except requests.exceptions.JSONDecodeError as json_decode_error:
        print(f'An error has occurred while trying to convert:'
              f'{json_decode_error}\n')
    finally:
        return json_data_obj


def main():
    response = requests.get('https://data.nasa.gov/resource/gh4g-9sfh.json')
    if response is None:
        print(f'A GET Request error has occurred: No given object.\n')
        return None
    if response.status_code != 200:
        print(f'The GET Request was NOT successful \n{response.status_code} [{response.reason}]\n')
        return response
    else:
        print(f'The GET request was successful \n{response.status_code}[{response.reason}]\n')
        return response
    json_data = response.json()

    # geolocation bounding box -- (left, bottom, right, top)
    bound_box_dict = {
        'Africa_MiddleEast_Meteorites': (-17.8, -35.2, 62.2, 37.6),
        'Europe_Meteorites': (-24.1, 36, 32, 71.1),
        'Upper_Asia_Meteorites': (32.2, 35.8, 190.4, 72.7),
        'Lower_Asia_Meteorites': (58.2, -9.9, 154, 38.6),
        'Australia_Meteorites': (112.9, -43.8, 154.3, -11.1),
        'North_America_Meteorites': (-168.2, 12.8, -52, 71.5),
        'South_America_Meteorites': (-81.2, -55.8, -34.4, 12.6)
    }

    db_connection = None
    try:
        db_name = 'filtered_meteorite_data1.db'
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        for key in bound_box_dict.items():
            db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {key} (
                name MASS,
                mass TEXT,
                reclat TEXT,
                reclong TEXT);''')

        db_connection.commit()


    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection was closed.')


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
