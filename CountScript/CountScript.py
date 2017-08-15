import arcpy
from arcpy import env

# Set overwrite
arcpy.env.overwriteOutput = True

# Set workspace
env.workspace = "C:/Users/jcarpenter/Desktop/CountScript/"

# Define variables
input = 'data.gdb/sites'
states = ['VA','NC','SC','GA','TN','MD','WV','PA','NJ','DE','NY','OH','KY','TX','AL']
progress = ['Rumored', 'Under Contract']

# Create temporary layers
arcpy.MakeFeatureLayer_management (input, "templyr")
arcpy.MakeFeatureLayer_management (input, "templyr2")

# Create lists
rlist = [] 
uclist = []

# Loop through the states list
for state in states:

    # SQL Queries
    query = '"Progress" = ' + "'" + progress[0] + "'" + 'And' + '"State" = ' + "'" + state + "'"
    query2 = '"Progress" = ' + "'" + progress[1] + "'" + 'And' + '"State" = ' + "'" + state + "'"

    # Select by Attributes
    arcpy.SelectLayerByAttribute_management ("templyr", "NEW_SELECTION", query)
    arcpy.SelectLayerByAttribute_management ("templyr2", "NEW_SELECTION", query2)

    # Get count of selection
    count = int(arcpy.GetCount_management("templyr").getOutput(0))
    count2 = int(arcpy.GetCount_management("templyr2").getOutput(0))

    # Append the counts to the lists
    rlist.append(count)
    uclist.append(count2)

# Specifying the table and fields that will have values provided
table = 'data.gdb/site_update'
fields = ['Progress','VA','NC','SC','GA','TN','MD','WV','PA','NJ','DE','NY','OH','KY','TX','AL','Total']

# Create update cursor for table 
with arcpy.da.UpdateCursor(table, fields) as cursor:
    
    for row in cursor:
        
        if row[0] == "Rumored": # If the first row is Rumored
            row[1] = rlist[0]
            row[2] = rlist[1]
            row[3] = rlist[2]
            row[4] = rlist[3]
            row[5] = rlist[4]
            row[6] = rlist[5]
            row[7] = rlist[6]
            row[8] = rlist[7]
            row[9] = rlist[8]
            row[10] = rlist[9]
            row[11] = rlist[10]
            row[12] = rlist[11]
            row[13] = rlist[12]
            row[14] = rlist[13]
            row[15] = rlist[14]
            row[16] = sum(rlist) # Total
            
        elif row[0] == "Under Contract": # If the first row is Under Contract
            row[1] = uclist[0]
            row[2] = uclist[1]
            row[3] = uclist[2]
            row[4] = uclist[3]
            row[5] = uclist[4]
            row[6] = uclist[5]
            row[7] = uclist[6]
            row[8] = uclist[7]
            row[9] = uclist[8]
            row[10] = uclist[9]
            row[11] = uclist[10]
            row[12] = uclist[11]
            row[13] = uclist[12]
            row[14] = uclist[13]
            row[15] = uclist[14]
            row[16] = sum(uclist) # Total
            
        # Populate the row
        cursor.updateRow(row)
            
# Set output variable
out_xls = "countstable.xls"

# Execute TableToExcel
arcpy.TableToExcel_conversion(table, out_xls)

print "DONE!"