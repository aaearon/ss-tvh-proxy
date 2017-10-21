import datetime
import json
import urllib.request


class AuthSign:
	def __init__(self, username, password):
		self.site = None
		self.username = username
		self.password = password

		self.expiration_date = None
		self.hash = None

		if self.site == 'viewmmasr':
			self.url = 'https://www.MMA-TV.net/loginForm.php'
		else:
			self.url = 'https://auth.smoothstreams.tv/hash_api.php'

	def fetch_hash(self):
		now = datetime.datetime.now()

		if self.hash is None or now > self.expiration_date:
			print('Hash is either none or may be expired. Getting a new one...')
			hash_url = f'{self.url}?username={self.username}&password={self.password}&site={self.site}'
			response = urllib.request.urlopen(hash_url)

			try:
				as_json = json.loads(response.read())

				if 'hash' in as_json:
					self.hash = as_json['hash']
					self.set_expiration_date(as_json['valid'])

			except Exception as e:
				print('error!')

		print(f'Returning hash {self.hash}')

	def set_expiration_date(self, minutes):
		now = datetime.datetime.now()
		self.expiration_date = now + datetime.timedelta(minutes=minutes - 1)
