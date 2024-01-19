import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


# Function to perform OCR on a PDF file
def ocr_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize a list to hold all extracted text
    extracted_texts = []

    # Loop through each page in the PDF
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_num]

        # Get the list of image objects
        image_list = page.get_images(full=True)

        # Perform OCR on each image
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Load it to PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Use pytesseract to do OCR on the image
            text = pytesseract.image_to_string(image)

            # Add the text to the list
            extracted_texts.append(text)

    # Close the document
    pdf_document.close()

    return extracted_texts


# Path to your PDF file
pdf_path = '/Users/ellioe03/Downloads/Screenshot 2024-01-19 at 14.07.27.pdf'

# Perform OCR on the PDF
texts = ocr_pdf(pdf_path)

# Print the extracted text from each image
for num, text in enumerate(texts, start=1):
    print(f"Text from image {num}:")
    print(text)
