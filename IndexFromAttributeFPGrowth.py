"""
Gives the index of which class it belongs too
Basically an input variable like "Private" is put into the function
Then the function returns the index of "workclass" which in this case is 1
"""


def getClassTypeIndex(classType):

	switcher = {
		"?": 0,
		"Federal-gov": 0,
		"Local-gov": 0,
		"Never-worked": 0,
		"Private": 0,
		"Self-emp-inc": 0,
		"Self-emp-not-inc": 0,
		"State-gov": 0,
		"Without-pay": 0,
		"10th": 1,
		"11th": 1,
		"11th": 1,
		"1st-4th": 1,
		"5th-6th": 1,
		"7th-8th": 1,
		"9th": 1,
		"Assoc-acdm": 1,
		"Assoc-voc": 1,
		"Bachelors": 1,
		"Doctorate": 1,
		"HS-grad": 1,
		"Masters": 1,
		"Preschool": 1,
		"Prof-school": 1,
		"Some-college": 1,
		"Divorced": 2,
		"Married-AF-spouse": 2,
		"Married-civ-spouse": 2,
		"Married-spouse-absent": 2,
		"Never-married": 2,
		"Separated": 2,
		"Widowed": 2,
		"?": 3,
		"Adm-clerical": 3,
		"Armed-Forces": 3,
		"Craft-repair": 3,
		"Exec-managerial": 3,
		"Farming-fishing": 3,
		"Handlers-cleaners": 3,
		"Machine-op-inspct": 3,
		"Other-service": 3,
		"Priv-house-serv": 3,
		"Prof-specialty": 3,
		"Protective-serv": 3,
		"Sales": 3,
		"Tech-support": 3,
		"Transport-moving": 3,
		"Husband": 4,
		"Not-in-family": 4,
		"Other-relative": 4,
		"Own-child": 4,
		"Unmarried": 4,
		"Wife": 4,
		"Amer-Indian-Eskimo": 5,
		"Asian-Pac-Islander": 5,
		"Black": 5,
		"Other": 5,
		"White": 5,
		"Female": 6,
		"Male": 6,
		"?": 7,
		"Cambodia": 7,
		"Canada": 7,
		"China": 7,
		"Columbia": 7,
		"Cuba": 7,
		"Dominican-Republic": 7,
		"Ecuador": 7,
		"El-Salvador": 7,
		"England": 7,
		"France": 7,
		"Germany": 7,
		"Greece": 7,
		"Guatemala": 7,
		"Haiti": 7,
		"Holand-Netherlands": 7,
		"Honduras": 7,
		"Hong": 7,
		"Hungary": 7,
		"India": 7,
		"Iran": 7,
		"Ireland": 7,
		"Italy": 7,
		"Jamaica": 7,
		"Japan": 7,
		"Laos": 7,
		"Mexico": 7,
		"Nicaragua": 7,
		"Outlying-US(Guam-USVI-etc)": 7,
		"Peru": 7,
		"Philippines": 7,
		"Poland": 7,
		"Portugal": 7,
		"Puerto-Rico": 7,
		"Scotland": 7,
		"South": 7,
		"Taiwan": 7,
		"Thailand": 7,
		"Trinadad&Tobago": 7,
		"United-States": 7,
		"Vietnam": 7,
		"Yugoslavia": 7,
		"<=50K": 8,
		">50K": 8
	}
	return switcher.get(classType, "")