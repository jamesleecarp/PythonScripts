# Select Zip Codes

# Import arcpy module, csv
import arcpy
import csv

# Set workspace
arcpy.env.overwriteOutput = True

# Local variables:
input = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

# Set CSV variable
csvFile = open(arcpy.GetParameterAsText(2), "rb")

# CSV Reader variables
csvReader = csv.reader(csvFile)
header = csvReader.next()
zipIndex = header.index("Zips")

# Empty List
list = []

# Loop through CSV
for row in csvReader:
    Zips = row[zipIndex]
    list.append('"' + "ZCTA5CE10" + '"' + " = " +"'"+ (Zips) +"'"+ " OR ")

# Set Query
query = ''.join(map(str, list))
query = query[:-4]

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(input, "zipCodesLayer")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management("zipCodesLayer", "NEW_SELECTION", query)

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management("zipCodesLayer", output)

# Add Layer to map document
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]  
addLayer = arcpy.mapping.Layer(output)
arcpy.mapping.AddLayer(df, addLayer)
