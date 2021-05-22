import aiohttp
import asyncio
import requests
import time
import pandas as pd
from config import *
import sys



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

	def __init__(self, username, password, 
				 base_url="https://www.trounceflow.com/api/v1/"): 
		"""Initialize an APIClient object."""
		self.base_url = base_url
		self.username = username
		self.password = password
		self.access_token = None
		self.refresh_token = None
		self.access_token = asyncio.run(self.get_access_token())['token']
#		self.__get_access_token()
		
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
			response.close()
		except requests.exceptions.RequestException as err_http:
			raise SystemExit('Access Denied: %s '%(err_http))
		except requests.exceptions.ConnectionError as err_cnn:
		    raise SystemExit('Connection Failed: %s '%(err_cnn))
		except requests.exceptions.Timeout as err_timeout:
		    raise SystemExit('Timeout: %s '%(err_timeout))
		
	async def get_access_token(self):
		async with aiohttp.ClientSession() as session:
			async with session.post(self.base_url + "auth-token/", 
					   data= {'username': self.username,'password': self.password}) as response:				
				return await response.json()
		
	async def fetch_ticker(self, session, ticker):
		url = URL_MAPPER[ticker]

		async with session.get(url, 
			headers= {'Authorization': 'Token '+self.access_token}) as response:
			results = await response.json()
			return pd.DataFrame(results).set_index('date').add_prefix(ticker.split(':')[0]+'_')
			
	async def __get_resource(self,tickers):
		async with aiohttp.ClientSession() as session:
			tasks = []
			for ticker in tickers:
				task = asyncio.ensure_future(self.fetch_ticker(session, ticker))
				tasks.append(task)
			rs = await asyncio.gather(*tasks)
			df = pd.concat(rs,axis=1)
		return df
		
	def get_resource(self,tickers, to_csv=None):
		if isinstance(tickers, list):
			df = asyncio.run(self.__get_resource(tickers))
		elif isinstance(tickers,str):
			df = asyncio.run(self.__get_resource([tickers]))
		else:
			return 'tickers type str or list'

		if to_csv:
			df.to_csv(to_csv)
		return df
		
	def get_direct_url(self,ticker):
		return URL_MAPPER[ticker]
	
	def get_meta_info(self,ticker):
		return
		
	def get_freq(self,ticker):
		return 
		#pd.infer_freq(index, warn=True)
