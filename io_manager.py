# This module manage all the I/O from files.

import os
import zipfile

class folder_management:

    @staticmethod
    def list_of_files_to_render():
        ''' Return a list with thes name of all the files in "IN" folder '''
        return os.listdir("IN")

    @staticmethod
    def import_xml_content(filename):
        xml_content = ""
        with zipfile.ZipFile(os.path.join("IN", filename)) as activinspire_zipped:
            xml_content = activinspire_zipped.open("content.xml", "r").read().decode('UTF-8')

        return xml_content

    @staticmethod
    def create_temp_svg_file(file_name, content_of_file):
        temp_file_path = os.path.join(os.getcwd(), "temp",  file_name[:-4] + ".svg")
        open(temp_file_path, "w+").write(content_of_file)
        
        return temp_file_path

    @staticmethod
    def delete_temp_svg_file(file_name):
        os.remove(file_name)
        return True 