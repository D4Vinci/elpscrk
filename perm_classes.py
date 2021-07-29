import phonenumbers
import time
from datetime import datetime
from itertools import product, chain, permutations as perm, zip_longest as zip


class data_plus:
	# using tuples instead of lists because it's faster and more efficient.
	# and generators are even more efficient (little memory usage, performance...)
	letters = tuple('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	digits = tuple('0123456789')
	chars = tuple(' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')  # owasp.org/www-community/password-special-characters
	years = lambda x: (str(yr) for yr in range(x, time.localtime().tm_year + 1))
	leet = {'a': '4', 'i': '1', 'e': '3', 't': '7', 'o': '0', 's': '5', 'g': '9', 'z': '2'}
	leet_perm = lambda word: (''.join(letters) for letters in
							  product(*({c, data_plus.leet.get(c, c)} for c in word)))  # yeah generator
	nums_range = lambda n: (str(num) for num in range(0, n + 1))


class names_perm:
	def __init__(self, names, complicated=0):
		if complicated >= 1:
			# all names permutations (lowercase, uppercase, capitalized, reversed)
			self.words = tuple(chain.from_iterable([(p.lower(), p.upper(), p.capitalize(), p[::-1]) for p in names]))
			# First letter in each name permutations
			self.one = tuple(chain.from_iterable([(p.lower(), p.upper()) for p in [name[0] for name in names]]))
			# First two letters in each name permutations
			self.two = tuple(chain.from_iterable(
				[(p.lower(), p.upper(), p.capitalize(), p[::-1]) for p in [name[:2] for name in names]]))
		else:
			self.words = tuple(chain.from_iterable([(p.lower(), p.capitalize()) for p in names]))
			self.one = tuple(chain.from_iterable([(p.lower(), p.upper()) for p in [name[0] for name in names]]))
			self.two = tuple(
				chain.from_iterable([(p.lower(), p.upper(), p.capitalize()) for p in [name[:2] for name in names]]))

	def add_keywords(self, keywords):
		self.words += tuple(chain.from_iterable([(p.lower(), p.capitalize()) for p in keywords]))


class dates_perm:
	# Considering that date format is dd-mm-yyyy as we agreed :3
	def __init__(self, dates, complicated=0):
		_converter = lambda date: datetime.strptime(date, '%d-%m-%Y')
		self.dates = tuple(_converter(date) for date in dates)
		self.days = tuple(chain.from_iterable((str(date.day) for date in self.dates)))
		self.months = tuple(chain.from_iterable((str(date.month) for date in self.dates)))
		self.years = tuple(chain.from_iterable([(yr, yr[-2:]) for yr in (str(date.year) for date in self.dates)]))
		if complicated >= 1:
			self.days += tuple([("0" + dd) for dd in self.days if len(dd) == 1])
			self.months += tuple([("0" + mm) for mm in self.months if len(mm) == 1])
			self.years += tuple([yr[-3:] for yr in (str(date.year) for date in self.dates)])
		self.full_dates, self.joined_dates = [], []
		for day in self.days:
			for month in self.months:
				for year in self.years:
					self.full_dates.append((day, month, year))
					self.joined_dates.append("".join([day, month, year]))


class phones_perm:
	def __init__(self, phones):
		# Phone number format: (+Countrycode)xxxxxxxxxx
		self.phones = tuple(phonenumbers.parse(phone) for phone in phones)
		self.national = tuple("0" + str(phone.national_number) for phone in self.phones)
		self.first_four = tuple(str(phone.national_number)[2:6] for phone in self.phones)
		self.last_four = tuple(str(phone.national_number)[:-4] for phone in self.phones)


class oldpwds:
	def __init__(self, passwords, complicated=0):
		self.passwords = tuple(''.join(l for l in pwd if l.isalnum()) for pwd in passwords)
		if complicated >= 2:
			self.passwords = tuple(
				chain.from_iterable([(p.lower(), p.upper(), p.capitalize(), p[::-1]) for p in self.passwords]))
