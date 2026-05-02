try:
    print("Attempting to import xhtml2pdf...")
    import xhtml2pdf
    print(f"xhtml2pdf imported successfully: {xhtml2pdf.__file__}")
    from xhtml2pdf import pisa
    print("pisa imported successfully")
except Exception as e:
    print(f"Error importing xhtml2pdf: {e}")

try:
    print("Attempting to import reportlab...")
    import reportlab
    print(f"reportlab imported successfully: {reportlab.__file__}")
except Exception as e:
    print(f"Error importing reportlab: {e}")
