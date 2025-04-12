import aspose.pdf as ap
import os

import subprocess

def rescale_pdf_ghostscript(input_path: str, output_path: str, pdf_name: str, resolution=72):
    """
    Rescale a PDF to A4 size using Ghostscript
    
    Args:
        input_path (str): Path to input PDF file
        output_path (str, optional): Path for output PDF. If None, adds 'a4_' prefix
        resolution (int, optional): Output resolution in DPI. Default 72
    """
    
    # Ghostscript command components
    gs_command = [
        "gs",
        "-q",  # Quiet mode
        "-o", str(output_path),
        "-sDEVICE=pdfwrite",
        f"-g{842}x{595}",  # A4 size in points (595x842)
        "-dPDFFitPage",
        "-dFIXEDMEDIA",
        f"-r{resolution}",
        str(input_path)
    ]
    
    try:
        # Run Ghostscript command
        result = subprocess.run(
            gs_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"Successfully created A4 PDF: {output_path}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error rescaling PDF: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Ghostscript not found. Please install Ghostscript first.")
        return False

# def change_pdf_page_size(input_pdf: str, output_pdf: str, pdf_name: str, new_width: float, new_height: float):
#     # Load the PDF file.
#     document = ap.Document(input_pdf)
#     pages = document.pages

#     for page in pages:
#         # Get original page dimensions
#         original_width = page.get_page_rect(True).width
#         original_height = page.get_page_rect(True).height

#         if not (abs(original_width - new_width) > 100 and abs(original_height - new_height) > 100):
#             print(f"SKIPPED: {pdf_name}")
#             return
#     document.save(output_pdf)
#     print(f"Successfully resized {pdf_name}.")

def main():
    # Example: Change to landscape A4 size (597.6 x 842.4 points)
    #new_width_points = 842.4
    #new_height_points = 597.6

    raw_data = "doe_pdfs\\old_format_incompatible"
    for folder in os.listdir(raw_data):
        year_folder = os.path.join(raw_data, folder)
        if not ("2020" in year_folder): ## choose specific year
            continue
        for filename in os.listdir(year_folder):
            pdf_file =  os.path.join(year_folder, filename)
            output_path = f"doe_pdfs\\old_format_resized\\{folder}\\{filename}"
            if not ("ncr" in filename): ## only convert NCR data
                continue
            if os.path.exists(pdf_file):
                #change_pdf_page_size(pdf_file, output_path, filename, new_width_points, new_height_points)
                rescale_pdf_ghostscript(pdf_file, output_path, filename)
            else:
                print(f"Error: PDF file '{pdf_file}' not found.")


if __name__ == "__main__":
    main()