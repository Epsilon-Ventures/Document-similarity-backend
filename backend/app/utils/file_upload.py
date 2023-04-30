from ..models import loaded_model as model
from io import BytesIO

def file_upload_embeddings(FileClass, file_obj):
  # THIS WAY OF READING RETRIEVED FILE FINALLY WORKED . It is InMemoryUploadFile , so it is read this way
  file_content_ioByte = file_obj.read()

  # this is still in BytesIO format , to retrieve it in string format , we need to do this
  file_text_bytes = BytesIO(file_content_ioByte)

  # file_text is byte object , to convert that into string, we need to call .decode() function
  file_text_string = file_text_bytes.getvalue().decode()

  # to convert the string into list
  file_text_question_list = file_text_string.split("\n")
  file_text_question_list = [item for item in file_text_question_list if item != ""]

  FileClass.ques_list = file_text_question_list

  # convert to embeddings
  embeddings = model.encode(file_text_question_list)

  return embeddings
