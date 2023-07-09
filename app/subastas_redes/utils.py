from django.core.files.storage import FileSystemStorage

def handle_uploaded_file(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    return file_url