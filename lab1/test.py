import arcpy
import os

# define default workspace
arcpy.env.workspace = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb"
arcpy.env.overwriteOutput = True
input_path = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb{layer_name}"
aprx = arcpy.mp.ArcGISProject(r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.aprx")
map_doc = aprx.listMaps()[0]

# define layers
address = input_path.format(layer_name=r"\Addresses")
lakes = input_path.format(layer_name=r"\Lakes_Reservoirs")
mosquito = input_path.format(layer_name=r"\Mosquito_Larva")
osmp = input_path.format(layer_name=r"\OSMP_Properties")
wetlands = input_path.format(layer_name=r"\Wetlands")


# Define Buffer
def buffer(buf_lyr):
    # ask user for buffer parameters
    buf_out_name = input("What is the name of the buffer output for the " + buf_lyr + " layer?")
    buf_dist_input = input("What is the buffer distance in feet?")
    buf_dist = buf_dist_input + " feet"

    # buffer analysis
    result = arcpy.Buffer_analysis(buf_lyr, buf_out_name, buf_dist)

    return buf_out_name;


# Define Intersect
def intersect(int_lyrs):
    # ask user to name output layer
    lyr_name = input("What is the desired name of the output intersect layer?")

    # run intersect operation on input layer
    arcpy.Intersect_analysis(int_lyrs, lyr_name)

    # return resulting output layer
    return lyr_name


# Define Main
def main():
    # Define variables
    int_lyrs = []
    buf_lyrs = [lakes, mosquito, wetlands, osmp]

    # Call buffer
    for lyr in buf_lyrs:
        out_buf_name=buffer(lyr)
        int_lyrs.append(out_buf_name)


    # Call Intersect
    output_lyr_name = intersect(int_lyrs)

    # Spatial Join
    arcpy.analysis.SpatialJoin(address, output_lyr_name, "WNV_Spatial")

    # Add new layer to map
    map_doc.addDataFromPath(r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb\WNV_Spatial")
    aprx.save()

    # Extra Credit
    WNV_Spatial = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb\WNV_Spatial"
    arcpy.Select_analysis(WNV_Spatial, 'selection', "Join_Count > 0")
    count_lyr = r"C:\Users\lbcem\Desktop\GIS305\lab1\WestNileOutbreak\WestNileOutbreak.gdb\selection"
    result = arcpy.GetCount_management(count_lyr)
    print("There are " + result[0] + " homes in the danger area.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
