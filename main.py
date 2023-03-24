from io_manager import folder_management
import yaml
import os

# TODO Sistemare commento iniziale
# PDFFromActivinspire, software by Fabio Rimondi
# Final goal: Read files from "IN" folder, extract the SVG and then output a PDF in "OUT" folder.

# TODO Verify if Inkscape exist in the system or is reachable

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    
list_of_files = []
def main_sequence():
    
    print("Reading all the files to convert..")
    for file_in in folder_management.list_of_files_to_render():
        if file_in.endswith(".iwb"):
            list_of_files.append(file_in)
            print("- Found: " + str(file_in) )

    print("Processing files")
    for file_in_list in list_of_files:
        print("Extracting " + str(file_in_list) + " file..")
        content_of_file = folder_management.import_xml_content(file_in_list)

        print("Deleting useless strings")
        for string_to_delete in config["to_delete_parts"]:
            content_of_file = content_of_file.replace(string_to_delete, '')
        
        print("Replacing propertary SVG blocks")
        for string_to_replace in config["to_substitute_parts"]:
            content_of_file = content_of_file.replace(string_to_replace["from"], string_to_replace["to"])

        print("Deleting the extra part")
        content_of_file = content_of_file.split(config["extra_part_to_delete"])[0]

        print("Cleaning from \"<svg viewbox>\" tag ")
        # Here need to be deleted the viewbox  svg tag that create problems with export in PDF. For doing so the string is splitted by any escape, and with the following 
        # instruction only the part next the problematic tag is saved. Of course need to be cleaned after removing the "</svg>" of the tag deleted.
        content_of_file = content_of_file.split("\n",8)[8]
        content_of_file = content_of_file[:-9]                      # Delete the last </svg>

        print("Creating the temp svg file for conversion")

        temp_svg_file = folder_management.create_temp_svg_file(file_name=file_in_list, content_of_file=content_of_file)

        print("Temp file saved in : " + str(temp_svg_file))

        # Converting the SVG extracted to PDF using INKScape
        print("Saving as PDF..")

        output_file = os.path.join("OUT", file_in_list[:-4] + ".pdf")
        os.system("inkscape --file=\"" + str(temp_svg_file) + "\" --without-gui --export-area-drawing --export-pdf=\"" + output_file + "\"")

        print("PDF Saved as " + str(output_file))
    
        print("Cleaning temp file..")
        folder_management.delete_temp_svg_file(temp_svg_file)

        print("------------------------")

main_sequence()