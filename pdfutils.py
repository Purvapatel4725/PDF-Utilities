import os
import PyPDF2
import shutil
from pathlib import Path

def display_pdfs(directory):
    """Displays all PDF files in the given directory."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the directory.")
    else:
        print("Available PDFs:")
        for idx, pdf in enumerate(pdf_files, start=1):
            print(f"{idx}. {pdf}")
    return pdf_files

def get_directory():
    """Prompts the user for a directory path."""
    while True:
        directory = input("Enter the directory path (or press Enter for the current directory): ").strip()
        if not directory:
            return os.getcwd()
        elif os.path.isdir(directory):
            return directory
        else:
            print("Invalid directory. Please try again.")

def rename_pdf(file_path):
    """Renames a PDF file."""
    try:
        new_name = input(f"Enter the new name for '{file_path}' (with .pdf extension): ").strip()
        if not new_name.endswith('.pdf'):
            print("Error: File name must end with .pdf")
            return
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"'{file_path}' renamed to '{new_path}'.")
    except Exception as e:
        print(f"Error renaming file: {e}")

def merge_pdfs(directory):
    """Merges two or more PDF files."""
    try:
        pdf_files = display_pdfs(directory)
        if len(pdf_files) < 2:
            print("Not enough PDFs to merge.")
            return
        print("Select PDFs to merge (comma-separated indices, e.g., 1,2,3): ")
        indices = input().split(',')
        selected_pdfs = [pdf_files[int(i) - 1] for i in indices if i.isdigit() and 0 < int(i) <= len(pdf_files)]
        if not selected_pdfs:
            print("No valid selections made.")
            return
        merger = PyPDF2.PdfMerger()
        for pdf in selected_pdfs:
            merger.append(os.path.join(directory, pdf))
        output_name = input("Enter the name for the merged PDF (with .pdf extension): ").strip()
        if not output_name.endswith('.pdf'):
            print("Error: File name must end with .pdf")
            return
        output_path = os.path.join(directory, output_name)
        merger.write(output_path)
        merger.close()
        print(f"Merged PDF created at: {output_path}")
    except Exception as e:
        print(f"Error during merging: {e}")

def split_pdf(directory):
    """Splits a PDF based on user selection."""
    try:
        pdf_files = display_pdfs(directory)
        if not pdf_files:
            return
        selection = int(input("Select a PDF to split (enter index): "))
        selected_pdf = pdf_files[selection - 1]
        pdf_path = os.path.join(directory, selected_pdf)
        reader = PyPDF2.PdfReader(pdf_path)
        
        print("\nSplit Menu:")
        print("1. Split into individual pages")
        print("2. Split by page ranges")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            for page_num in range(len(reader.pages)):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_num])
                output_name = f"{Path(selected_pdf).stem}_page_{page_num + 1}.pdf"
                output_path = os.path.join(directory, output_name)
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            print(f"PDF split into individual pages in directory: {directory}")
        elif choice == '2':
            ranges = input("Enter page ranges to split (e.g., 1-3,4-6): ").strip()
            for range_pair in ranges.split(','):
                start, end = map(int, range_pair.split('-'))
                writer = PyPDF2.PdfWriter()
                for page_num in range(start - 1, end):
                    writer.add_page(reader.pages[page_num])
                output_name = f"{Path(selected_pdf).stem}_pages_{start}_to_{end}.pdf"
                output_path = os.path.join(directory, output_name)
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            print(f"PDF split by ranges and saved in directory: {directory}")
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error during splitting: {e}")

def watermark_pdf(directory):
    """Adds a watermark to each page of a PDF."""
    try:
        pdf_files = display_pdfs(directory)
        if not pdf_files:
            return
        selection = int(input("Select a PDF to watermark (enter index): "))
        selected_pdf = pdf_files[selection - 1]
        pdf_path = os.path.join(directory, selected_pdf)

        watermark_path = input("Enter the path to the watermark PDF: ").strip()
        if not os.path.exists(watermark_path):
            print("Watermark PDF not found.")
            return

        reader = PyPDF2.PdfReader(pdf_path)
        watermark_reader = PyPDF2.PdfReader(watermark_path)
        watermark_page = watermark_reader.pages[0]

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        output_name = f"{Path(selected_pdf).stem}_watermarked.pdf"
        output_path = os.path.join(directory, output_name)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        print(f"Watermarked PDF saved as: {output_path}")
    except Exception as e:
        print(f"Error during watermarking: {e}")

def compress_pdf(directory):
    """Compresses a PDF to reduce file size."""
    try:
        pdf_files = display_pdfs(directory)
        if not pdf_files:
            return
        selection = int(input("Select a PDF to compress (enter index): "))
        selected_pdf = pdf_files[selection - 1]
        pdf_path = os.path.join(directory, selected_pdf)

        reader = PyPDF2.PdfReader(pdf_path)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_name = f"{Path(selected_pdf).stem}_compressed.pdf"
        output_path = os.path.join(directory, output_name)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"Compressed PDF saved as: {output_path}")
    except Exception as e:
        print(f"Error during compression: {e}")

def main_menu():
    """Main menu for PDF processing."""
    while True:
        print("\nPDF Processor Menu")
        print("1. Merge PDFs")
        print("2. Split PDF")
        print("3. Add Watermark")
        print("4. Compress PDF")
        print("5. Rename PDF")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            directory = get_directory()
            merge_pdfs(directory)
        elif choice == '2':
            directory = get_directory()
            split_pdf(directory)
        elif choice == '3':
            directory = get_directory()
            watermark_pdf(directory)
        elif choice == '4':
            directory = get_directory()
            compress_pdf(directory)
        elif choice == '5':
            directory = get_directory()
            pdf_files = display_pdfs(directory)
            if pdf_files:
                selection = int(input("Select a PDF to rename (enter index): "))
                rename_pdf(os.path.join(directory, pdf_files[selection - 1]))
        elif choice == '6':
            print("Exiting PDF Processor. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
