from sentence_transformers import SentenceTransformer

loaded_model = None

# Create your models here.
def load_model():
  """Returns the loaded model

  Returns:
      class: The loaded sentence transformer model
  """
  global loaded_model
  if not loaded_model:
    loaded_model = SentenceTransformer("Nischal2015/sbert_eng_ques")
  return loaded_model
