import os
import fitz
import box
import yaml
from pdf2image import convert_from_path

def parse_api_call(request):
    """Parses an API call request, validates its format and content, and returns a response dictionary."""

    # Check if request is JSON and is correct
    if request.is_json and request.data:
        # Check if JSON data can be read
        try:
            json_request = request.get_json()
        except: # pylint: disable=bare-except
            return {"status": "error", "data": request, "message": "Request should be in JSON format."}

        # Check if filepath was provided
        if 'filepath' not in json_request:
            return {"status": "error", "data": request, "message": "Request is missing filepath attribute."}

        # Check if filepath is a string
        if not isinstance(json_request['filepath'], str):
            return {"status": "error", "data": request, "message" : "Attribute filepath contains invalid value."}

    else:
        return  {"status": "error", "data": request, "message":"Request should be in JSON format."}

    return {"status": "success", "data": {"info": json_request, "request": request}, "message": None}

def get_extension_from_filepath(filepath):
    """Get extension from filepath"""

    parts = filepath.split('.')
    if len(parts) > 1:
        return parts[-1]

    return ""

def get_filename_from_filepath(filepath):
    """Get filename from filepath (without file extension)"""

    filename_with_extension = os.path.basename(filepath)
    filename = filename_with_extension.split(".")[0]

    return filename

def is_valid_filepath(filepath):
    """Returns True if filepath is valid, else returns False"""

    if os.path.exists(filepath):
        return True

    return False

def pdf_to_images_with_adjust_dpis(filepath, dest_folder, dpi=300, ext='.jpg', codec='JPEG'):
    """Convert PDF file to image with the possibility of adjusting dpis"""

    # Open pdf
    pdf_file = fitz.open(filepath)

    # Get filename to later save images in folder
    filename = get_filename_from_filepath(filepath)

    # Define interval of pages to handle
    range_start = 0
    range_end = pdf_file.page_count

    image_paths = []
    for page_num in range(range_start, range_end):
        page = pdf_file[page_num]
        w_ratio = 612/page.rect.width # Using A4 size as reference
        h_ratio = 792/page.rect.height # Using A4 size as reference
        new_dpi = int(w_ratio*dpi) if w_ratio < h_ratio else int(h_ratio*dpi)

        # Store pdf with convert_from_path function
        images = convert_from_path(filepath, dpi=new_dpi, first_page=page_num+1, last_page=page_num+1, use_pdftocairo=True)

        j = 0
        for i in range(page_num, page_num+len(images)):
            image_path = f'{dest_folder}{filename}-{str(i)}{ext}'
            # Save pages as images in the pdf
            images[j].save(image_path, codec)
            image_paths.append(image_path)
            j += 1

    pdf_file.close()

    return image_paths

def get_config_vars(config_path):
    with open(config_path, 'r', encoding='utf8') as ymlfile:
        config = box.Box(yaml.safe_load(ymlfile))

    return config
