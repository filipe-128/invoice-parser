from flask import Flask, request
from src.utils import parse_api_call
from src.model import invoice_parser_chain
from src.ocr import start_paddle_ocr
from src.parser import validate_openai_api_key

# Start Flask
app = Flask(__name__)

# Start OCR model
ocr_engine = start_paddle_ocr()

# Check if API key is available
validate_openai_api_key()

print("Ready to receive requests")

@app.post("/parse")
def parse_invoice():
    """Ingests a pdf or image of an invoice and parses the data."""
    output = {}, 500
    try:
        # Parse request
        parsed_request = parse_api_call(request)

        # Request is successful, run chain
        if parsed_request["status"] == "success":
            output = invoice_parser_chain(parsed_request["data"]["info"], ocr_engine)
            print(f"Finished request with {output[0]['status']}")

            return output

        # Request returned an error, return
        return {"ERROR": parsed_request["message"], "status": "error", "data": "", "message": parsed_request["message"]}, 400

    except Exception: # pylint: disable=broad-exception-caught
        return {"ERROR": "Internal Server Error", "status": "error", "data": output,
                "message": "Something went wrong while trying to extract information from the document... Please try again."}, 500
