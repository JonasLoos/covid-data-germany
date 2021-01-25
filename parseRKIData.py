# This file is used to download and parse new data from the RKI.
# Data Source: Robert Koch-Institut (RKI), dl-de/by-2-0
# Run with Python3: `python parseRKIData.py` or `python3 parseRKIData.py`.

# imports
import numpy as np  # install using `pip install numpy` or `pip3 install numpy`
from datetime import date
import requests



# default config
download = True
input_file = 'Covid-19_Infektionen_pro_Tag.csv'
output_file_cases = f'cases/{date.today()}.csv'
output_file_deaths = f'deaths/{date.today()}.csv'
maximum_number_of_days_to_assume = 3*365


# constants
AGS = [1001,1002,1003,1004,1051,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,2000,3101,3102,3103,3151,3153,3154,3155,3157,3158,3159,3241,3251,3252,3254,3255,3256,3257,3351,3352,3353,3354,3355,3356,3357,3358,3359,3360,3361,3401,3402,3403,3404,3405,3451,3452,3453,3454,3455,3456,3457,3458,3459,3460,3461,3462,4011,4012,5111,5112,5113,5114,5116,5117,5119,5120,5122,5124,5154,5158,5162,5166,5170,5314,5315,5316,5334,5358,5362,5366,5370,5374,5378,5382,5512,5513,5515,5554,5558,5562,5566,5570,5711,5754,5758,5762,5766,5770,5774,5911,5913,5914,5915,5916,5954,5958,5962,5966,5970,5974,5978,6411,6412,6413,6414,6431,6432,6433,6434,6435,6436,6437,6438,6439,6440,6531,6532,6533,6534,6535,6611,6631,6632,6633,6634,6635,6636,7111,7131,7132,7133,7134,7135,7137,7138,7140,7141,7143,7211,7231,7232,7233,7235,7311,7312,7313,7314,7315,7316,7317,7318,7319,7320,7331,7332,7333,7334,7335,7336,7337,7338,7339,7340,8111,8115,8116,8117,8118,8119,8121,8125,8126,8127,8128,8135,8136,8211,8212,8215,8216,8221,8222,8225,8226,8231,8235,8236,8237,8311,8315,8316,8317,8325,8326,8327,8335,8336,8337,8415,8416,8417,8421,8425,8426,8435,8436,8437,9161,9162,9163,9171,9172,9173,9174,9175,9176,9177,9178,9179,9180,9181,9182,9183,9184,9185,9186,9187,9188,9189,9190,9261,9262,9263,9271,9272,9273,9274,9275,9276,9277,9278,9279,9361,9362,9363,9371,9372,9373,9374,9375,9376,9377,9461,9462,9463,9464,9471,9472,9473,9474,9475,9476,9477,9478,9479,9561,9562,9563,9564,9565,9571,9572,9573,9574,9575,9576,9577,9661,9662,9663,9671,9672,9673,9674,9675,9676,9677,9678,9679,9761,9762,9763,9764,9771,9772,9773,9774,9775,9776,9777,9778,9779,9780,10041,10042,10043,10044,10045,10046,11000,12051,12052,12053,12054,12060,12061,12062,12063,12064,12065,12066,12067,12068,12069,12070,12071,12072,12073,13003,13004,13071,13072,13073,13074,13075,13076,14511,14521,14522,14523,14524,14612,14625,14626,14627,14628,14713,14729,14730,15001,15002,15003,15081,15082,15083,15084,15085,15086,15087,15088,15089,15090,15091,16051,16052,16053,16054,16055,16056,16061,16062,16063,16064,16065,16066,16067,16068,16069,16070,16071,16072,16073,16074,16075,16076,16077]


def RKIdownload():
	# download the data file from the RKI
	try:
		with open(input_file, mode='wb') as f:
			print('downloading new data from RKI...')
			f.write(requests.get('https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv').content)
	except requests.exceptions.ConnectionError as e:
		print('Could not download file (no internet?)')
		exit()


def RKIparse(input_file=input_file, output_file_cases=output_file_cases, output_file_deaths=output_file_deaths):
	# create result matrices
	cases = np.zeros((len(AGS)+1,maximum_number_of_days_to_assume+1), dtype=int)
	day0 = date(2019,1,1).toordinal()  # ==737425, this is the first day
	cases[0,1:] = np.arange(start=day0, stop=day0+maximum_number_of_days_to_assume)
	deaths = cases.copy()

	# init
	print(f'parsing new data: {input_file}')
	firstDayFound = 1000000  # some very high number
	lastDayFound = -1

	# open file
	with open(input_file) as f:
		# read lines (ignore the header line and the last empty line)
		lines = [line.split(',') for line in f.readlines()[:-1]]

	# init AGS
	cases[1:,0] = np.array(AGS)  # write the Landkreis-id to the first column
	deaths[1:,0] = np.array(AGS)  # write the Landkreis-id to the first column

	# read column indexes
	new_cases_i = lines[0].index('AnzahlFall')
	new_deaths_i = lines[0].index('AnzahlTodesfall')
	ags_i = lines[0].index('IdLandkreis')
	date_i = lines[0].index('Meldedatum')
	lines = lines[1:]  # cut off header line

	# go through lines
	for i, entries in enumerate(lines):

		# available Columns:
		# ObjectId IdBundesland Bundesland Landkreis Altersgruppe Geschlecht AnzahlFall AnzahlTodesfall Meldedatum IdLandkreis Datenstand NeuerFall NeuerTodesfall Refdatum NeuGenesen AnzahlGenesen IstErkrankungsbeginn Altersgruppe2
		# explanations: https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74

		# AnzahlFall: Anzahl der Fälle in der entsprechenden Gruppe
		new_cases = int(entries[new_cases_i])
		# AnzahlTodesfall: Anzahl der Todesfälle in der entsprechenden Gruppe
		new_deaths = int(entries[new_deaths_i])
		# Landkreis ID: Id des Landkreises des Falles in der üblichen Kodierung 1001 bis 16077=LK Altenburger Land
		ags = fixBerlin(int(entries[ags_i]))
		# Meldedatum: Datum, wann der Fall dem Gesundheitsamt bekannt geworden ist
		date_str = entries[date_i][:10]
		date_obj = date(int(date_str[:4]),int(date_str[5:7]),int(date_str[8:]))
		day = date_obj.toordinal() - day0
		if day < 0:
			# all reported cases should be after or on day0
			print('Error: day == {} <= 0 ({}); skipping line {} ({} case[s])'.format(day, date_obj, i, new_cases))
			continue

		# convert landkreis to index
		if ags in AGS:
			ags_index = AGS.index(ags)+1
		else:
			print('Error: unknown ags {}; skipping line {} ({} case[s])'.format(ags, i, new_cases))
			continue

		# set min/max dates
		if day < firstDayFound: firstDayFound = day
		if day > lastDayFound: lastDayFound = day

		# save data
		cases[ags_index,day+1] += new_cases
		deaths[ags_index,day+1] += new_deaths
		# cases_by_age[age_index, ags_index, day] += new_cases

	print('  found data from {} until {}'.format(date.fromordinal(firstDayFound+day0), date.fromordinal(lastDayFound+day0)))
	# check for errors
	assert firstDayFound >= 0, "Error: Found Cases before `day0`, which were not ignored."
	tmp = np.absolute(cases[1:,1:]).sum(axis=1)>0  # use absolute to not panic when finding zombies (deaths that are later reverted, happened e.g. in 3402 Emden)
	assert all(tmp), "It seems like some data is missing ({} ags have no cases) {}".format(len(AGS)-tmp.sum(),"".join("\nline {}: {}".format(i, AGS[i]) for i in range(len(AGS)) if not tmp[i]))
	tmp = np.absolute(deaths[1:,1:]).sum(axis=1)>0
	assert all(tmp), "It seems like some data is missing ({} ags have no deaths): {}".format(len(AGS)-tmp.sum(), "".join("\nline {}: {}".format(i, AGS[i]) for i in range(len(AGS)) if not tmp[i]))

	# cut off the future
	cases = cases[:,:lastDayFound+1]
	deaths = deaths[:,:lastDayFound+1]

	# save csv
	np.savetxt(output_file_cases, cases, delimiter=',', fmt='%d')
	np.savetxt(output_file_deaths, deaths, delimiter=',', fmt='%d')


def fixBerlin(landkreis):
	# Berlin is splitted in RKI data but not in population data
	# so set all parts of Berlin equal to Berlin itself
	return 11000 if 11000 <= landkreis <= 11012 else landkreis


if __name__ == "__main__":
	if download:
		RKIdownload()
	RKIparse()
