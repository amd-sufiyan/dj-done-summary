from bs4 import BeautifulSoup
import random
import time
from pathlib import Path
from datetime import datetime
import requests
# from utils import get_free_proxy, get_one_porxy_work, SDRespToData2
from .core import resp2dataframe2, WriteInDatabase, WriteInXlsx, WriteInDjDoneSummary
from torpy.http.requests import tor_requests_session
from frontpage.models import DoneSummary


hasil_test_path = Path() / 'hasil_test' 
log_file = Path() / 'log.txt'
headers = { 
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
   'X-Requested-With': 'XMLHttpRequest'
}


delay = 5 # 
saham_code = [ 'bbca', 'jmas', 'pkpk', 'bfin', "poly", "jast", "issp", "brms"]
# saham_code = ["issp", "brms"]

# if not hasil_test_path.exists():
# 	hasil_test_path.mkdir(parents=True, exist_ok=True)


def let_scrape():
	now = datetime.now()
	now_format = now.strftime('%b-%d-%Y %H-%M-%S')
	# hasil_test_path_format = hasil_test_path / str(now_format)
	# if not hasil_test_path_format.exists():
	# 	hasil_test_path_format.mkdir(parents=True, exist_ok=True)

	print(f"Start again... : {now_format}")

	try:
		# a = 5 / 0
		with tor_requests_session() as s:  # returns requests.Session() object

			def get_summary(code):
				url = f'https://www.indopremier.com/module/saham/include/data-donesummary.php?code={code}'
				res = s.get(url, headers=headers, timeout=3)
				timestamp = datetime.now()
				return (code, timestamp, res)

			print(s.get('http://httpbin.org/ip', timeout=3).json())
			random.shuffle(saham_code)

			responses = []
			for code in saham_code:
				res = get_summary(code)
				print('use tor ',res)
				responses.append(res)
	except Exception as e:
		with requests.Session() as sess:
			responses = []
			for code in saham_code:
				now_time = datetime.now().strftime('%H:%M:%S')

				url = f'https://www.indopremier.com/module/saham/include/data-donesummary.php?code={code}'
				url = f'http://127.0.0.1:8080/{code.upper()}.html'
				res = sess.get(url, headers=headers, timeout=3)
				timestamp = datetime.now()
				resp = (code, timestamp, res)
				print('asli ', resp)
				responses.append(resp)

	dataframe = resp2dataframe2(responses)
	_ = WriteInDjDoneSummary(dataframe)

