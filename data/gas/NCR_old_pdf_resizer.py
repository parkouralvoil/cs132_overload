import aspose.pdf as ap
import pdf2image
import img2pdf
from PIL import Image
import os
import io

def change_pdf_page_size(input_pdf: str, output_pdf: str, pdf_name: str, new_width: float, new_height: float):
    # Load the PDF file.
    document = ap.Document(input_pdf)
    pages = document.pages

    scale_fac = 1
    for page in pages:
        # Get original page dimensions
        original_width = page.get_page_rect(True).width
        original_height = page.get_page_rect(True).height

        if not (abs(original_width - new_width) > 100 and abs(original_height - new_height) > 100):
            print(f"SKIPPED: {pdf_name}")
            return
        # Calculate scale factors
        scale_x = new_width / original_width
        scale_y = new_height / original_height

        scale_fac = max(scale_x, scale_y)
    rescale_pdf_raster(input_pdf, output_pdf, scale_fac)

        # Save the modified PDF.
        #document.save(output_pdf)
    print(f"Successfully resized {pdf_name}.")

def rescale_pdf_raster(input_path: str, output_path: str, scale_factor: float, dpi=300):
    # Convert PDF to images
    images = pdf2image.convert_from_path(
            input_path,
            dpi=dpi,
            fmt='jpeg',  # Explicit format
            thread_count=4,  # Multi-threading for faster processing
        )
    
    # Process images
    processed_images = []
    for img in images:
        # Convert to RGB if needed (JPEG doesn't support alpha)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize with anti-aliasing
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        resized_img = img.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        processed_images.append(img_byte_arr.read())
    
    # Convert back to PDF
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(processed_images))

def main():
    # Example: Change to landscape A4 size (597.6 x 842.4 points)
    new_width_points = 842.4
    new_height_points = 597.6

    raw_data = "doe_pdfs\\old_format"
    for folder in os.listdir(raw_data):
        year_folder = os.path.join(raw_data, folder)
        if not ("2023" in year_folder): ## choose specific year
            continue
        for filename in os.listdir(year_folder):
            pdf_file =  os.path.join(year_folder, filename)
            output_path = f"doe_pdfs\\old_format_resized\\{folder}\\{filename}"
            if not ("ncr" in filename): ## only convert NCR data
                continue
            if os.path.exists(pdf_file):
                change_pdf_page_size(pdf_file, output_path, filename, new_width_points, new_height_points)
            else:
                print(f"Error: PDF file '{pdf_file}' not found.")


if __name__ == "__main__":
    main()