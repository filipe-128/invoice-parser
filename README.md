# Invoice Parser

Invoice Parser is a Python-based application designed to extract and process information from invoice documents. The tool leverages OCR technology to convert scanned invoices into structured data for further analysis and processing.

## Features

- **OCR Integration**: Uses PaddleOCR to read text from images.
- **Data Extraction**: Identifies invoices and extracts relevant information contained in the invoice.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/filipe-128/invoice-parser.git
   cd invoice-parser
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables:
Create a .env file in the root directory of the project and add your OpenAI API key:
   ```sh
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

1. Place the invoice images in the `docs` folder. Available formats are .pdf, .png and .jpg.

2. Run the main application with filepath argument:
   ```sh
   python main.py --filepath "docs/example.png"
   ```

3. Extracted data will be displayed in a JSON format.

## Configuration

- Modify `config.yaml` to change the temporary folder directory or the OpenAI model to use. Available models are listed [here](https://platform.openai.com/docs/models).

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.
