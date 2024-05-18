import os
from src.utils import (get_extension_from_filepath,
                       is_valid_filepath,
                       pdf_to_images_with_adjust_dpis,
                       get_config_vars
                      )
from src.ocr import run_paddle_ocr

class Document:
    def __init__(self, filepath):
        self.filepath = filepath
        self.temp_dir = ""
        self.filetype = get_extension_from_filepath(filepath)
        self.images = []
        self.content = []

    def create_temp_dir(self, config_path):
        self.temp_dir = get_config_vars(config_path)['TEMP_PATH']
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def convert_pdf_to_images(self):
        """
        Converts pdf to images, saves to destination folder
        """
        print(f"Converting PDF at {self.filepath} to images...")

        self.images = pdf_to_images_with_adjust_dpis(self.filepath, self.temp_dir)
        print(self.images)
        print('------------------')

    def run_ocr_engine(self, ocr_engine):
        """Runs the OCR engine and obtains dictionary with results for each image"""
        for image_path in self.images:
            print(f"Extracting text from {image_path}...")

            result = run_paddle_ocr(image_path, self.temp_dir, ocr_engine)
            self.content.append(result)
        print('------------------')

    def erase_temp_imgs(self):
        """Delete temp files created during processing"""
        for imgpath in self.images:
            os.remove(imgpath)
        os.remove(f'{self.temp_dir}ocr_result.jpg')


def invoice_parser_chain(filepath_dic, ocr_engine):
    """Chain to process document and return parsed data"""

    # Validate filepath
    filepath = filepath_dic['filepath']
    if not is_valid_filepath(filepath):
        return {"ERROR": "Filepath not valid.", "status": "error", "data": "",
        "message": "The filepath provided is not valid. Please check and try again."}, 422

    # Initiate a document object
    doc = Document(filepath)

    # Create temp dir to store files
    doc.create_temp_dir(config_path="config.yaml")

    # Convert file from pdf to image
    if doc.filetype == 'pdf':
        # Convert pdf to images
        doc.convert_pdf_to_images()
    elif doc.filetype in ['png', 'jpg']:
        doc.images = [filepath]
    else:
        return {"ERROR": "Filetype not valid.", "status": "error", "data": "",
        "message": "The filetype provided is not valid. Valid options: 'pdf', 'png', 'jpg'."}, 422

    # Run the OCR engine to extract content
    doc.run_ocr_engine(ocr_engine)

    # Erase temporary files created during processing
    doc.erase_temp_imgs()

    return {"status": "success", "data": doc.content, "message": None}, 200
