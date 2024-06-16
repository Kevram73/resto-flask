import os, uuid
from werkzeug.utils import secure_filename

class FileManager:
    ALLOWED_EXTENSIONS = {'webp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    init_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self,file_folder):
        self.file_folder = file_folder

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def remove_suffix_from_path(self, original_path):
    
        # Ensure the path is treated as a raw string
        suffix = 'controller'
        original_path = os.path.abspath(original_path)
        original_path = rf"{original_path}"
        
        # Check if the original path ends with the specified suffix
        if original_path.endswith(suffix):
            # Calculate the new path by removing the suffix
            new_path = original_path[:-len(suffix)-1]
            return new_path
        else:
            return original_path
    
    def base_folder(self):
        init_path = self.remove_suffix_from_path(self.init_path)
        return os.path.join(init_path, 'static', 'admin', 'images', self.file_folder)

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
            folder = self.base_folder()
            try:
                # Ensure the upload folder exists
                if not os.path.exists(folder):
                    os.makedirs(folder)
                file.save(os.path.join(folder, filename))
                return filename, 'File successfully saved.'
            except Exception as e:
                return None, f'Error saving file: {str(e)}'
        return None, 'File type not allowed.'

    def delete_file(self, filename):
        file_path = os.path.join(self.base_folder(), filename)
        print(file_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True, 'File successfully deleted.'
            except Exception as e:
                return False, f'Error deleting file: {str(e)}'
        else:
            return False, 'File not found.'