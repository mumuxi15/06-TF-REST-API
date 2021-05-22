import os
import json
import asyncio
import hashlib
import requests
import pandas as pd
#from .config import *
from config import *

from time import time

# #########   Exceptions     #############

class AuthException(ValueError):
	"""Auth process exception."""
	def __init__(self, backend, *args, **kwargs):
		self.backend = backend
		super().__init__(*args, **kwargs)


class AuthFailed(AuthException):
	"""Auth process failed for some reason."""
	def __str__(self):
		msg = super().__str__()
		return 'Authentication failed: {0}'.format(msg)


class AuthTokenError(AuthException):
	"""Auth token error."""
	def __str__(self):
		msg = super().__str__()
		return 'Token error: {0}'.format(msg)

# #########   API    #############
class APIClient(object):

	session = requests.Session()

	def __init__(self, username, password, base_url="https://www.trounceflow.com/api/v1/"):  ###client_key, secret_key
		"""Initialize an APIClient object."""
		self.base_url = base_url
		self.username = username
		self.password = password
		self.access_token = None
		self.refresh_token = None

		self.__get_access_token()

#		self.credentials = Credentials(client_key=client_key, secret_key=secret_key)
	def sign(self, key, msg):
		"""Get the digest of the message using the specified key."""
		return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


	def __get_access_token(self):
		""" create token """
		response = requests.post(
			url  = self.base_url + "auth-token/",
			data = {
				'username': self.username,
				'password': self.password
			}
		)
		try:
			response.raise_for_status()
			self.access_token = response.json()['token']
			# additional code will only run if request is successful
		except requests.exceptions.RequestException as err_http:
			raise SystemExit('Access Denied: %s '%(err_http))
		except requests.exceptions.ConnectionError as err_cnn:
		    raise SystemExit('Connection Failed: %s '%(err_cnn))
		except requests.exceptions.Timeout as err_timeout:
		    raise SystemExit('Timeout: %s '%(err_timeout))

	def get_main_network_headers():
	    headers = {
	        "nethash": "bc669a7d8a4ce656d1acd326d694ef6a45ae181e93b57505170bcc26ddb7b98c", #hashed address
	        "version": "1.0.1",
	        "port": "4001"
	    }
	    return headers

	def set_token(self,token=None):  # this is a bypass, potential security prob ???
		self.access_token = token

	def refresh_token(self):
		self.__get_access_token()

	def __load_ticker(self,ticker):
		response = requests.get(URL_MAPPER[ticker], headers= {'Authorization': 'Token '+self.access_token})
		if response.ok:
			df = pd.DataFrame(json.loads(response.text)).set_index('date')
			df.index = pd.to_datetime(df.index)
			return df
		else:
			print ('Data request denied,  {0}'.format(URL_MAPPER[ticker]))
			return pd.DataFrame()


	def load_data(self,tickers,start_date=None,end_date=None):
		if self.access_token:			
			df = list(map(self.__load_ticker, tickers))
			df = pd.concat(df,axis=1)
#			print (df)
			df = df.apply(pd.to_numeric)
			if start_date:
				df = df.loc[df.index>start_date]
			if end_date:
				df= df.loc[df.index<end_date]
		else:
			return 'Token Error, please use set_token(token='') function'


