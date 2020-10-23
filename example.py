from sarpy.io.complex.converter import open_complex

reader = open_complex(str(input("Insert SICD file: ")))
# this provides an instance of one of the reader classes defined in the modules in sarpy.io.complex
# a sicd file will necessarily be composed of a single image, but other file formats
# (sentinel, radarsat, others) often contain multiple images combined into a single
# package (i.e. multiple polarizations or other aggregate collections)


################
# SICD metadata structure
# Access the single SICD structure or tuple of structures associated with the reader
# Note that the sicd structure is defined using elements of sarpy.io.complex.sicd_elements

nebulous_contents = reader.sicd_meta
# this will be an instance of the sicd structure, or a tuple of sicd structures
# (if multiple images)

# Unified access - this will always be a tuple of sicd structures,
# with one sicd structure per image
sicd_tuple = reader.get_sicds_as_tuple()

the_sicd = sicd_tuple[0]  # access the desired sicd structure
# provide a human readable, if long, contents to terminal
print(the_sicd)
# get xml string representation
xml_string = the_sicd.to_xml_string(tag='SICD')
# get json friendly dict representation
dict_representation = the_sicd.to_dict()

# access field values
print(the_sicd.CollectionInfo.CollectorName)

###############
# Read complex pixel data from file - use slice notation
# data = reader[row_start:row_end:row_step, col_start:col_end:col_step, image_index=0]

# in the event of a single image segment
all_data = reader[:]  # or reader[:, :] - reads all data
decimated_data = reader[::10, ::10] # reads every 10th pixel

# in the event of multiple image segments - use another slice index (defaults to 0)
# the image segment index defaults to 0 for multi-segment images

all_data = reader[:, :, 0]  # reads all data from the image segment at index 0
# = reader[:, :], reader[:] - yields same result, since image index defaults to 0


#################
# Show some basic plots of the data
from matplotlib import pyplot
import sarpy.visualization.remap as remap

fig, axs = pyplot.subplots(nrows=1, ncols=3, figsize=(12, 4))
axs[0].imshow(remap.density(reader[::10, ::10]), cmap='gray')
# Reads every other row and column from the first thousand rows and columns:
axs[1].imshow(remap.density(reader[:1000:2, :1000:2]), cmap='gray')  # Display subsampled image
# Reads every row and column from the first thousand rows and columns:
axs[2].imshow(remap.density(reader[0:1000, 0:1000]), cmap='gray')  # Display subsampled image
pyplot.show()


##############
# Convert a complex dataset (in any format handled by SarPy) to SICD

from sarpy.io.complex.converter import conversion_utility
# to SICD format
conversion_utility('<complex format file>', '<output_directory>')
# to SIO format
conversion_utility('<complex format file>', '<output_directory>', output_format='sio')
