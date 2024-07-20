import psutil
import sys
import time
import click
from perm_classes import *
from utils import *


class main_ganerator:
	def __init__(self, level=0, pwd_min=8, pwd_max=12, num_range=0,
				 leeter=False, years=0, chars=True, verbose=True, export='passwords.txt'):
		# Complication levels:
		# 0 = default
		# 1 = 0 + allowing more permutations in perm_classes
		# 2 = 1 + allowing more permutations in old passwords perm class
		# 3 = 2 + Using the whole special chars set allowed in passwords
		# 4 = 3 + Use more permutations in the main function
		# 5 = 4 + Don't use ordered pairs for perm function
		# if you want more, enable the leeter it's level 666 lol!
		self.shit_level   = level
		self.verbose_mode = verbose
		# Okay lesgooo!
		self.names = names_perm
		self.dates = dates_perm
		self.phones = phones_perm
		self.old_passwords = oldpwds
		self.total_result = []
		# Password length variables
		self.minimum_length = pwd_min
		self.maximum_length = pwd_max
		# Deepness level
		# For banner and checking
		self.number_range = f"{B}{num_range}{reset + W}" if num_range != 0 else f"{R}False{reset + W}"
		self.years_range = f"{B}{years}-{time.localtime().tm_year + 1}{reset + W}" if years != 0 else f"{R}False{reset + W}"
		if chars:
			self.special_chars = f"{B}All chars{reset + W}" if self.shit_level >= 3 else f"{B}Common chars{reset + W}"
		else:
			self.special_chars = f"{R}False{reset + W}"
		self.leeting = f"{B}Enabled{reset + W}" if leeter else f"{R}Disabled{reset + W}"
		# For looping
		self.recipes = [[]]
		if num_range != 0:
			self.recipes.append(data_plus.nums_range(num_range))
		if years != 0:
			self.recipes.append(data_plus.years(years))
		if chars:
			if self.shit_level >= 3:
				self.recipes.append(data_plus.chars)
			else:
				self.recipes.append(("_", ".", "-", "!", "@", "*", "$", "?", "&",
									 "%"))  # Common special chars according to this thread (https://www.reddit.com/r/dataisbeautiful/comments/2vfgvh/most_frequentlyused_special_characters_in_10/)
		self.add_leet_perms = leeter
		self.export_file = export

	def __input(self, prompt):
		result = []
		while True:
			print(f"{G}[{reset + B}>{reset + G}] {prompt}{reset}", end="")
			data = input()
			print(f"{reset}", end="")
			if data:
				if " " in data.strip():
					data = data.split(" ")
				else:
					data = [data]
				for part in data:
					for smaller_part in part.split(","):
						if smaller_part:
							result.append(smaller_part)
			return result


	def __pwd_check(self, pwd):
		if (len(pwd) >= self.minimum_length) and (len(pwd) <= self.maximum_length) and (pwd not in self.total_result):
			return True
		return False

	def __simple_perm(self, target, *groups):
		for pair in zip(*groups, fillvalue=""):
			for targeted in target:
				pair = (targeted,) + pair
				for addition in self.recipes:
					yield ("".join(pair + (added,)) for added in addition)

	def __commonPerms(self):
		# Just to make sure common perms are in permutations
		for name in self.names.words:
			if self.__pwd_check(name):
				self.total_result.append(name)
		for date in self.dates.joined_dates:
			if self.__pwd_check(date):
				self.total_result.append(date)
			for thing in [self.names.words, self.names.one, self.names.two]:
				for justone in thing:
					if self.__pwd_check(justone + date):
						self.total_result.append(justone + date)
		for national_number in self.phones.national:
			if self.__pwd_check(national_number):
				self.total_result.append(national_number)
			for thing in [self.names.words, self.names.one, self.names.two]:
				for justone in thing:
					if self.__pwd_check(justone + national_number):
						self.total_result.append(justone + national_number)

	def __perm(self, target, *groups, perm_length=None):
		# Return all the permutations of a combined iterators/generators
		if groups:
			perm_length = perm_length if perm_length else len(groups) + 1
			if self.shit_level >= 5:
				# You want more results,
				#      don't wanna skip any possible permutation,
				#          and you don't mind more unrealistic results?
				#              Then you came for the right place :laughing:
				for pair in ((target, pair2) for pair2 in groups):
					for addition in self.recipes:
						iterator = chain.from_iterable(pair + (addition,))
						yield ("".join(p) for p in perm(iterator, perm_length) if
							   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))
			else:
				# If you want things not complicated for more realistic results, use ordered pairs like this
				# Maybe I'm wrong? PR with what you think is best realistic result without chaos :)
				for targeted in target:
					for pair in (((targeted,) + pairs) for pairs in zip(*groups, fillvalue="")):
						for addition in self.recipes:
							if not addition:
								yield ("".join(p) for p in perm(pair, perm_length) if
									   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))
							else:
								for added in addition:
									# iterator = chain.from_iterable(pair+(added,))
									iterator = pair + (added,)
									yield ("".join(p) for p in perm(iterator, perm_length) if
										   (self.__pwd_check("".join(p)) and not ("".join(p)).isdecimal()))

	def __perms(self, *main_group, others, perm_length=None):
		# Return the combined permutations of (main_group, other_group)
		# Written this one to make the code cleaner instead of writting self.__perm many times
		iters = []
		for other_group in others:
			iters.append(self.__perm(*main_group, other_group, perm_length=perm_length))
		iters.append(self.__perm(*main_group, *others, perm_length=perm_length))
		return chain.from_iterable(iters)

	def __export(self):
		# Line by line is slower but memeory efficient (very large results could not fit in your ram)
		if self.total_result:
			sys.stdout.write(f"[~] Exporting results to {self.export_file}...\r")
			sys.stdout.flush()
			with open(self.export_file, 'w') as f:
				for pwd in self.total_result:
					f.write(f"{pwd}\n")
			print(f"[+] Results exported to {self.export_file}!")

	def perms_generator(self):
		self.__commonPerms()
		mixes = [
			self.__simple_perm(self.names.words, ),
			self.__perms(self.names.words, others=(self.dates.days, self.dates.months, self.dates.years), ),
			self.__perm(self.names.one, self.dates.joined_dates, ),
			self.__perm(self.names.two, self.dates.joined_dates, ),
			self.__perms(self.names.words, others=(self.phones.national, self.phones.first_four, self.phones.last_four), ),
			self.__perm(self.names.one, self.phones.national, ),
			self.__perm(self.names.two, self.phones.national, ),
			self.__perms(self.names.one, others=(self.phones.first_four, self.phones.last_four), ),
			self.__perms(self.names.two, others=(self.phones.first_four, self.phones.last_four), ),
			self.__perm(self.names.words, self.dates.years, self.phones.first_four, ),
			self.__perm(self.names.words, self.dates.years, self.phones.last_four, ),
			self.__perm(self.names.words, self.dates.years, self.phones.national, )
		]

		# Added combination of names and nicknames
		for name in self.names.words:
			for nickname in self.nicknames:
				combined_name_nickname = name + nickname
				if self.__pwd_check(combined_name_nickname):
					self.total_result.append(combined_name_nickname)
		
		if self.old_passwords.passwords:
			for pwd in self.old_passwords.passwords:
				for iterator in (data_plus.nums_range(100), data_plus.years(1900), data_plus.chars,):
					mixes.append(("".join(p) for one in iterator for p in perm((pwd, one), 2) if self.__pwd_check("".join(p))))
			mixes.append(self.__perm(self.old_passwords.passwords, self.names.words, ))
			mixes.append(self.__perms(self.old_passwords.passwords, others=(self.dates.days, self.dates.months, self.dates.years), ))
			mixes.append(self.__perms(self.old_passwords.passwords, others=(self.phones.national, self.phones.first_four, self.phones.last_four), ))
		
		if self.shit_level >= 4:
			mixes.append(self.__perm(self.names.words, self.dates.days, self.dates.months, self.dates.years))
			mixes.append(self.__perm(self.names.one, self.names.two, self.dates.joined_dates))
			mixes.append(self.__perm(self.names.words, self.phones.first_four, self.phones.last_four))
			mixes.append(self.__perm(self.names.one, self.names.two, self.phones.national))
			mixes.append(self.__perm(self.names.one, self.names.two, self.phones.first_four, self.phones.last_four, ))
			mixes.append(self.__perm(self.names.words, self.dates.years, self.phones.first_four, self.phones.last_four, ))
			mixes.append(self.__perm(self.names.words, self.dates.days, self.dates.months, self.phones.national, ))
			mixes.append(self.__perm(self.dates.days, self.dates.months, self.dates.years, ))
			mixes.append(self.__perm(self.phones.national, self.dates.years, ))
			mixes.append(self.__perm(self.phones.first_four, self.phones.last_four, self.dates.years, ))

		sys.stdout.write("[~] Generating passwords...\r")
		sys.stdout.flush()
		for generator in chain.from_iterable(mixes):
			for pwd in generator:
				if self.__pwd_check(pwd):
					self.total_result.append(pwd)
					if self.verbose_mode:
						sys.stdout.write(f"[~] Generating passwords: {pwd : <25} [N:{len(self.total_result) :_<10}]\r")
						sys.stdout.flush()

		print(f"[+] Total number: {str(len(self.total_result))+' password(s)': <40}")
		self.__export()
		if self.add_leet_perms:
			print("[~] Now making new file with leet permutations for each generated password...")
			del self.total_result[:]
			self.total_result = []
			with open(self.export_file, 'r') as data:
				for pwd in data:
					self.total_result.extend(data_plus.leet_perm(pwd.strip()))
			self.export_file = "Leeted-"+self.export_file
			print(f"[+] Total number of leeted passwords: {len(self.total_result)} password(s)")
			self.__export()

	def __print_banner(self):
		with open("banner.txt") as f:
			banner_text = f.read()
			print(W + banner_text.format(
				ver=f"{reset}{B}2.0{reset}{W}",
				num=self.number_range, year=self.years_range,
				chars=self.special_chars,
				leet=self.leeting,
				min=f"{reset}{B}{self.minimum_length}{reset}{G}", max=f"{reset}{B}{self.maximum_length}{reset}{G}",
				verbose={
					True: f"{B}Enabled{reset + W}",
					False: f"{R}Disabled{reset + W}"
				}[self.verbose_mode], export=f"{B}{self.export_file}{reset + W}",
				# 0 = default
				# 1 = 0 + allowing more permutations in perm_classes
				# 2 = 1 + allowing more permutations in old passwords perm class
				# 3 = 2 + Using the whole special chars set allowed in passwords
				# 4 = 3 + Don't use ordered pairs for perm function
				# 5 = 4 + Use more permutations in the main function
				level=reset+C+{
					0: "Simple person",
					1: "Average person",
					2: "Cyber awareness ",
					3: "Paranoid person",
					4: "Nerd person",
					5: "Nuclear!",
				}[self.shit_level]+reset+G,
				G=G, end=reset + W
			) + reset)

	def interface(self):
		self.__print_banner()
		self.names = self.names(self.__input("Any names (No spaces, comma separated): "), complicated=self.shit_level)
		self.nicknames = self.__input("Any nicknames (No spaces, comma separated): ")  # Added line
		self.names.add_keywords(self.__input("Any keywords like nicknames, job, movies, series... (No spaces, comma separated): "))
		self.dates = self.dates(self.__input("Any birthdays or dates you know (Format: [dd-mm-yyyy], comma separated): "), complicated=self.shit_level)
		self.phones = self.phones(self.__input("Any phone numbers you know (Format: [+Countrycodexxx...], comma separated): "))
		self.old_passwords = self.old_passwords(self.__input("Old passwords or words you think new passwords will be made out of it (comma separated): "), complicated=self.shit_level)
		start_time = time.time()
		try:
			self.perms_generator()
		except KeyboardInterrupt:
			print('[!] Detected Keyboard interruption(Ctrl+C)! Exiting...')
			self.__export()
		finally:
			process = psutil.Process(os.getpid())
			elapsed = round(time.time()-start_time, 2)
			if elapsed >= 60:
				elapsed /= 60
				elapsed = str(round(elapsed, 2))+"m"
			else:
				elapsed = str(elapsed)+"s"
			print(f"[+] Elapsed time {elapsed} - Memory usage (rss:{round(process.memory_info().rss / 1024 ** 2, 2)}MB vms:{round(process.memory_info().vms / 1024 ** 2, 2)}MB)")
			sys.exit(0)

@click.command()
@click.option('-l', '--level', metavar='', type=click.Choice(['0', '1', '2', '3', '4', '5']), default='0', help='Level of complication of passwords.')
@click.option('--min', 'pmin', metavar='', type=int, default=8, help='Minimum length of passwords to generate (Default:8).')
@click.option('--max', 'pmax', metavar='', type=int, default=12, help='Maximum length of passwords to generate (Default:12).')
@click.option('-r', '--num-range', metavar='', type=int, default=0, help='Range of number to add to the mix (Start from 0 to the one you specify).')
@click.option('--leet', metavar='', is_flag=True, default=False, help='Gets all the Leet permutations of passwords after finish in a different file.')
@click.option('-y', '--years', metavar='', type=int, default=0, help='Adds to the mix all years from the given one to the next year we are in.')
@click.option('-c', '--chars', metavar='', is_flag=True, default=False, help='Adds the common special characters to the mix, but at level 3 and above it uses the whole special chars set allowed in passwords.')
@click.option('-v', '--verbose', metavar='', is_flag=True, default=False, help='Enables verbose mode so all passwords are printed to you while being generated (elpscrk will take double the time to finish).')
@click.option('-x', '--export', metavar='', type=str, default='passwords.txt', help='Name of the file to export results to it.')
def main(level, pmin, pmax, num_range, leet, years, chars, verbose, export):
	gen = main_ganerator(int(level), pmin, pmax, num_range, leet, years, chars, verbose, export)
	gen.interface()


if __name__ == '__main__':
	main()
