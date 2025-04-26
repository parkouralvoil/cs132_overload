how to use:

0. Make folders "doe_pdfs", "doe_word", "doe_csvs", and "compiled_csvs"

1. Download PDFs first with NCR_pump_prices_download.py

2. Go through the PDFs manually, check which ones do not have the overall table data (2nd table, the one below the main table) and separate them accordingly

3. Run NCR_pump_prices_convert

4. To process the PDFs without overall table data, follow these steps: (make sure to create the necessary folders each file needs)
    1. run NCR_old_pdf_resizer*
    2. run NCR_old_prices_save_docs*
    3. run NCR_old_prices_get_csv*
    4. run old_summarizer*

5. compile all the individual datas by running compiler_by_year*

6. compile all the compiled datas by running compiler_all

7. interpolate the data with interpolater.py (you may need to edit the code here and uncomment some lines under if __name__ == "__main__":)


*Note: you may need to edit the code to make it work on all year folders instead of having it work on only one year folder when u run the code.