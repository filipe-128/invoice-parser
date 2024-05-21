import argparse
import sys
from src.model import invoice_parser_chain
from src.ocr import start_paddle_ocr
from src.parser import validate_openai_api_key

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',
                        type=str,
                        required=True,
                        help='Enter the filepath of the document you want to parse')
    args = parser.parse_args()

    # Start OCR model
    ocr_engine = start_paddle_ocr()

    # Check if API key is available
    api_output = validate_openai_api_key()
    if api_output is not True:
        if 'status' in api_output[0] and api_output[0]['status'] == "error":
            print(api_output)
            sys.exit(0)

    OUTPUT = invoice_parser_chain({'filepath': args.filepath}, ocr_engine)
    print(OUTPUT)
