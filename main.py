import argparse
from src.model import invoice_parser_chain
from src.ocr import start_paddle_ocr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',
                        type=str,
                        required=True,
                        help='Enter the filepath of the document you want to parse')
    args = parser.parse_args()

    # Start OCR model
    ocr_engine = start_paddle_ocr()

    OUTPUT = invoice_parser_chain({'filepath': args.filepath}, ocr_engine)
    print(OUTPUT)
