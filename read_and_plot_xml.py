import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up some plotting parameters
sns.set(rc={'figure.figsize': (8, 4)})
sns.set(style="white")
sns.set_palette(['#439630', '#371447'])


"""
===================
xml parser function
===================

Takes an xml file and returns a list of category and x/y coordinates for each
kernel.
"""


def parse_xml(input_xml):

	# Make element tree for object
	tree = ET.parse(input_xml)

	# Getting the root of the tree
	root = tree.getroot()

	# Pulling out the name of the image
	image_name_string = root[0][0].text

	# Pulling out the fluorescent and non-fluorescent children
	fluorescent = root[1][1]
	nonfluorescent = root[1][2]

	# Setting up some empty lists to move the coordinates from the xml into
	fluor_x = []
	fluor_y = []
	nonfluor_x = []
	nonfluor_y = []

	# Getting the coordinates of the fluorescent kernels
	for child in fluorescent:
		if child.tag == 'Marker':
			fluor_x.append(child.find('MarkerX').text)
			fluor_y.append(child.find('MarkerY').text)

	# Getting the coordinates of the non-fluorescent kernels
	for child in nonfluorescent:
		if child.tag == 'Marker':
			nonfluor_x.append(child.find('MarkerX').text)
			nonfluor_y.append(child.find('MarkerY').text)

	# Formatting the results for output
	ear_name = image_name_string.rstrip('.png')

	fluor_string_col = ['fluorescent'] * len(fluor_x)
	ear_name_string = [ear_name] * len(fluor_x)
	fluor_coord = np.column_stack((ear_name_string, fluor_string_col, fluor_x, fluor_y))

	ear_name_string = [ear_name] * len(nonfluor_x)
	nonfluor_string_col = ['non-fluorescent'] * len(nonfluor_x)
	nonfluor_coord = np.column_stack((ear_name_string, nonfluor_string_col, nonfluor_x, nonfluor_y))

	# Appending the matrices together
	return_df = np.vstack((fluor_coord, nonfluor_coord))

	# Convert to pandas dataframe
	return_df = pd.DataFrame(return_df,
								columns=['ear_name', 'seed_type', 'x_coord', 'y_coord'])

	# Converting coord columns to numerics
	return_df['x_coord'] = pd.to_numeric(return_df['x_coord'])
	return_df['y_coord'] = pd.to_numeric(return_df['y_coord'])

	# Returning the results
	return return_df


# Running the xml parsing
coordinates = parse_xml('/Users/CiderBones/Desktop/Laboratory/r_projects/computer_vision/'
						'xml_files_transmission_defect_x415-499 _red_tape/X401x491L-2m1.xml')

# Making a little plot. Still need to figure out the white space issues
sns.scatterplot(x='x_coord', y='y_coord', hue='seed_type', data=coordinates)
sns.despine()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.axis('equal')
plt.ylim(0, 750)
plt.show()

# Test comment