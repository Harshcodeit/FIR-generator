from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None

def load_embeddings(
        model_name : str = 'sentence-transformers/all-MiniLM-L6-v2'        
) :
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name = model_name
        )
    return _embedding_model

