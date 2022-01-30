import random
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3 as sqlite
import xlsxwriter
from frontpage.models import DoneSummary

class SDRespToData2(object):
    """Like SDRespToData But with timestamp value
    """
    def __init__(self, resp=None):
        (self.code, self.timestamp, self.res) = resp
        soup = BeautifulSoup(self.res.text, 'html.parser')
        table = soup.find('table')

        self.thead_label = []
        for tr in table.find('thead').find_all('th'):
            self.thead_label.append(tr.get_text().strip())

        rows = table.find('tbody').find_all('tr')

        self.table_data = []
        for row in rows:
            row_data = []
            for td in row.find_all('td'):
                td_data = td.get_text().strip()
                row_data.append(td_data)
            if not (not all(row_data)):
                # timestamp = timestamp.strftime()
                self.table_data.append(row_data)

    def get_data(self):
        return self.table_data

    def get_thead_label(self):
        return self.thead_label

class SDRespToDj(object):
    """Like SDRespToData But with timestamp value
    """
    def __init__(self, resp=None):
        (self.code, self.timestamp, self.res) = resp
        soup = BeautifulSoup(self.res.text, 'html.parser')
        table = soup.find('table')

        self.thead_label = []
        for tr in table.find('thead').find_all('th'):
            self.thead_label.append(tr.get_text().strip())

        rows = table.find('tbody').find_all('tr')

        self.table_data = []
        for row in rows:
            row_data = []
            for td in row.find_all('td'):
                td_data = td.get_text().strip()
                row_data.append(td_data)
            if not (not all(row_data)):
                # timestamp = timestamp.strftime()
                self.table_data.append(row_data)

    def get_data(self):
        return self.table_data

    def get_thead_label(self):
        return self.thead_label



def resp2dataframe2(responses=None):
    if responses is None:
        return
    dataframe = []
    for resp in responses:
        (code, timestamp, res) = resp
        if res.status_code == 200:
            data = SDRespToData2(resp)
            dataframe.append(data)
    return dataframe

class WriteInDatabase(object):
    def __init__(self, dataframe=None):
        if dataframe is None:
            pass

        data_path = Path() / 'data'
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        now_f = now.strftime("%d %b %Y %H,%M")
        db_path = data_path / f'shm {now_f}.db'

        with sqlite.connect(str(db_path)) as conn:
            for data in dataframe:
                # CREATE_STMT = "CREATE TABLE IF NOT EXISTS tracks (id INTEGER PRIMARY KEY, Date TIMESTAMP, price INTEGER, description text, description text)"
                CREATE_STMT = f"CREATE TABLE IF NOT EXISTS {data.code} (id INTEGER PRIMARY KEY, Date TIMESTAMP, Price TEXT, B_Lot TEXT, S_Lot TEXT, T_Lot TEXT, B_Frq TEXT, S_Frq TEXT, T_Frq TEXT )"
                INSERT_STMT = f"INSERT INTO {data.code} VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)"

                cur = conn.cursor()
                create_table = cur.execute(CREATE_STMT)


                for row in data.get_data():
                    conn.execute(INSERT_STMT, row)
                conn.commit()
                cur.close()

class WriteInXlsx(object):
    def __init__(self, dataframe=None):
        if dataframe is None:
            pass

        data_path = Path() / 'data'
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        now_f = now.strftime("%d %b %Y %H,%M")
        xlsx_path = data_path / f'shm {now_f}.xlsx'

        workbook = xlsxwriter.Workbook(str(xlsx_path), {'strings_to_numbers': True})
        # Add some cell formats.
        integer = workbook.add_format({'num_format': '0'})
        decimal = workbook.add_format({'num_format': '0.00', 'align': 'center'})
        percentage = workbook.add_format({'num_format': '0.0%', 'align': 'center'})

        zebra = workbook.add_format({'bold': True})

        for obj in dataframe:
            worksheet = workbook.add_worksheet(obj.code)
            worksheet.write_row(f'A1', obj.get_thead_label(), zebra)
            print(obj.get_data())
            for i, row in enumerate(obj.get_data(), 2):
                worksheet.write_row(f'A{i}', row, integer)

            # worksheet.conditional_format('A2:H12', {'type': 'cell',
            #                                          'criteria': '==',
            #                                          'value': 0,
            #                                          'format': zebra})
        workbook.close()

class WriteInDjDoneSummary(object):
    def __init__(self, dataframe=None):
        if dataframe is None:
            pass

        for obj in dataframe:
            label = ["Price", "B_Lot", "S_Lot", "T_Lot", "B_Frq", "S_Frq", "T_Frq",]
            obj_list = []
            for row in obj.get_data():
                kwargs = dict(zip(label, row))
                added = {
                    # "ip": obj.res.raw._connection.sock.getsockname(),
                    "code": obj.code}
                kwargs.update(added)
                obj = DoneSummary(**kwargs)
                obj_list.append(obj)
            DoneSummary.objects.bulk_create(obj_list)

        # for x in DoneSummary.objects.all():
        #     print(x)


