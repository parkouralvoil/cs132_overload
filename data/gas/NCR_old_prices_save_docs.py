import os
import comtypes.client

# python -m NCR_old_prices_save_docs

def open_pdf_in_word(pdf_path: str, docx_path: str):
    """
    Opens a PDF file directly in Microsoft Word.  This relies on Word's ability to
    open PDF files, which may not always produce perfect results.

    Args:
        pdf_path (str): The path to the PDF file.
    """
    try:
        # Check if the PDF file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Error: PDF file not found at {pdf_path}")

        # Open the PDF file using Microsoft Word
        #subprocess.run(['start', 'winword', pdf_path], shell=True)
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = True  # Make Word visible to see what's happening
        doc = word.Documents.Open(os.path.join(os.getcwd(), pdf_path))  # Open the PDF
        # time.sleep(2)  # Give Word a moment to process, may need adjustment
        doc.SaveAs(os.path.join(os.getcwd(), docx_path), FileFormat=16)  # 16 = wdFormatXMLDocument (.docx)
        doc.Close()
        word.Quit()

        ## now print the last 2 columns
        print(f"Successfully saved to {docx_path} using COM automation.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    raw_data = "doe_pdfs\\old_format_resized"
    for folder in os.listdir(raw_data):
        year_folder = os.path.join(raw_data, folder)
        if not ("2021" in year_folder): ## choose specific year
            continue
        for filename in os.listdir(year_folder):
            pdf_file =  os.path.join(year_folder, filename)
            csv_path = f"doe_csvs\\{folder}\\{filename.replace(".pdf", ".csv")}"
            output_path = f"doe_word\\{folder}\\{filename.replace(".pdf", ".docx")}"
            if not ("ncr" in filename): ## only convert NCR data
                continue
            if os.path.exists(output_path):
                print(f"Skipped {output_path}")
                continue
            if os.path.exists(pdf_file):
                open_pdf_in_word(pdf_file, output_path)
            else:
                print(f"Error: PDF file '{pdf_file}' not found.")