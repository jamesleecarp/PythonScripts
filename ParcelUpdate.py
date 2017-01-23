# Final Project - ParcelUpdate Script

# Import arcpy module
import arcpy

# Input and Output Workspace
arcpy.env.workspace = "C:\\Users\\jcarpenter\\Documents\\PennState\\Geog485\\FinalProject"
arcpy.env.overwriteOutput = True
Output_gdb = "Output.gdb"

# Input Variables
Parcels = "Data.gdb\\Parcels"
Zoning = "Data.gdb\\Zoning"

# Layers
Parcels_Layer = "Parcels_Layer"
Parcels_Output_Layer = Parcels_Layer
Parcel_Centerpoints_Joined_Layer = "Parcel_Centerpoints_Joined_L"

# Output Variables
Parcels_Output = "Output.gdb\\Parcels"
Parcel_Centerpoints = "Data.gdb\\Parcel_Centerpoints_Inside"
Parcel_Centerpoints_Joined = "Data.gdb\\Parcel_Centerpoints_Joined"

# Mapping Variables
source = "ZoningParcels.lyr"
mapDocument1 = "Parcels.mxd"
mapDocument2 = "ParcelsUpdate2.mxd"
mapDocument3 = "ParcelsUpdate3.mxd"
mapDocument4 = "ParcelsUpdate.mxd"
pdf = "Parcels Map.pdf"
pdf2 = "ParcelsUpdate Map.pdf"

# Parameters
v_Inside_ = "true"
Join_Operation__ONE_TO_MANY_ = "JOIN_ONE_TO_MANY"
Field_Map ="\
OBJECTID \"OBJECTID\" true true false 8 Double 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.OBJECTID,-1,-1;\
PIN14 \"PIN14\" true true false 14 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.PIN14,-1,-1;\
PIN10 \"PIN10\" true true false 10 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.PIN10,-1,-1;\
L_ADDR \"L_ADDR\" true true false 8 Double 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.L_ADDR,-1,-1;\
H_ADDR \"H_ADDR\" true true false 8 Double 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.H_ADDR,-1,-1;\
PRE_DIR \"PRE_DIR\" true true false 1 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.PRE_DIR,-1,-1;\
ST_NAME \"ST_NAME\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ST_NAME,-1,-1;\
ST_TYPE \"ST_TYPE\" true true false 5 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ST_TYPE,-1,-1;\
SUF_DIR \"SUF_DIR\" true true false 10 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.SUF_DIR,-1,-1;\
STREET \"STREET\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.STREET,-1,-1;\
STREET_NUM \"STREET_NUM\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.STREET_NUM,-1,-1;\
ZONE_CLASS \"ZONE_CLASS\" true true false 254 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ZONE_CLASS,-1,-1;\
PD_NUM \"PD_NUM\" true true false 8 Double 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.PD_NUM,-1,-1;\
EDIT_DATE \"date_edit_\" true true false 8 Date 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.EDIT_DATE,-1,-1;\
ORDINANCE1 \"date_ordin\" true true false 8 Date 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ORDINANCE1,-1,-1;\
ORDINANCE_ \"ordinance\" true true false 254 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ORDINANCE_,-1,-1;\
PD_PREFIX \"PD_PREFIX\" true true false 254 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.PD_PREFIX,-1,-1;\
ZONE_TYPE \"ZONE_TYPE\" true true false 8 Double 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ZONE_TYPE,-1,-1;\
ORD_DATE \"ORD_DATE\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ORD_DATE,-1,-1;\
ORD_NUM \"ORD_NUM\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ORD_NUM,-1,-1;\
ZONE \"ZONE\" true true false 50 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.ZONE,-1,-1;\
More_Infor \"More_Infor\" true true false 200 Text 0 0 ,First,#,Parcels_Layer,Parcel_Centerpoints_Joined.More_Infor,-1,-1"
# Name \"Alias\" ALLOW NULL VALUES Default Value length type precision scale, Merge Rule, layer, table_dataset (input field), start_position, end_position

# Tool Script
try:
    # Process 1: Make Feature Layer 1
    arcpy.MakeFeatureLayer_management(Parcels, Parcels_Layer, "", "", "")

    # Process 2: Feature To Point
    arcpy.FeatureToPoint_management(Parcels, Parcel_Centerpoints, v_Inside_)
    
    # Process 3: Spatial Join
    arcpy.SpatialJoin_analysis(Parcel_Centerpoints, Zoning, Parcel_Centerpoints_Joined, Join_Operation__ONE_TO_MANY_, "KEEP_ALL", "", "INTERSECT", "", "")

    # Process 4: Make Feature Layer 2
    arcpy.MakeFeatureLayer_management(Parcel_Centerpoints_Joined, Parcel_Centerpoints_Joined_Layer, "", "", "")

    # Process 5: Add Join
    arcpy.AddJoin_management(Parcels_Layer, "PIN14", Parcel_Centerpoints_Joined_Layer, "PIN14", "KEEP_COMMON")

    # Process 6: Feature Class to Feature Class
    arcpy.FeatureClassToFeatureClass_conversion(Parcels_Output_Layer, Output_gdb, "Parcels", "", Field_Map, "")

    # Process 7: Delete excess centerpoint data
    arcpy.Delete_management(Parcel_Centerpoints)
    arcpy.Delete_management(Parcel_Centerpoints_Joined)
    
except:
    # Report an error messages
    arcpy.AddError("Could not complete Tool")
 
    # Report any error messages that the script might have generated    
    arcpy.AddMessage(arcpy.GetMessages())

# Map Script
try:
    # Reference layer
    sourceLayer = arcpy.mapping.Layer(source)

    # Add layer in map document
    mxd = arcpy.mapping.MapDocument(mapDocument1)
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    addLayer = arcpy.mapping.Layer(Parcels_Output)
    arcpy.mapping.AddLayer(df, addLayer, "TOP")
    mxd.saveACopy(mapDocument2)

    # Update layer
    mxd2 = arcpy.mapping.MapDocument(mapDocument2)
    updateLayer = arcpy.mapping.ListLayers(mxd2, "Parcels", df) [0]
    arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, True)
    # Update legend
    lyr = arcpy.mapping.ListLayers(mxd, 'Parcels', df)[0]
    styleItem = arcpy.mapping.ListStyleItems("ESRI.style", "Legend Items", "Horizontal Single Symbol Layer Name and Label")[0]
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    legend.updateItem(lyr, styleItem)
    mxd.saveACopy(mapDocument3)

    # Remove zoning layer in map document
    mxd3 = arcpy.mapping.MapDocument(mapDocument3)
    for df2 in arcpy.mapping.ListDataFrames(mxd):
        for lyr in arcpy.mapping.ListLayers(mxd, "", df2):
            if lyr.name.lower() == "zoning":
                arcpy.mapping.RemoveLayer(df, lyr)
            if lyr.name.lower() == "blank parcels":
                arcpy.mapping.RemoveLayer(df, lyr)
    mxd.saveACopy(mapDocument4)

    # Export to pdf
    mxd = arcpy.mapping.MapDocument(mapDocument1)
    arcpy.mapping.ExportToPDF(mxd, pdf)
    mxd4 = arcpy.mapping.MapDocument(mapDocument4)
    arcpy.mapping.ExportToPDF(mxd4, pdf2)

except:
    # Report an error messages
    arcpy.AddError("Could not complete Map")
 
    # Report any error messages that the script might have generated    
    arcpy.AddMessage(arcpy.GetMessages())