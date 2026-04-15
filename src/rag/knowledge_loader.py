from langchain_community.document_loaders import WikipediaLoader

def load_knowledge(query):
    try:
        loader = WikipediaLoader(query=query, load_max_docs=1)
        docs = loader.load()
        return docs[0].page_content if docs else ""
    except:
        return ""