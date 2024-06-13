import os
# Import the open ai library
import openai
# import pdf loader from langchain_community
from langchain_community.document_loaders import PyPDFLoader
# Import load_dotenv and find_dotenv from dotenv
from dotenv import load_dotenv, find_dotenv
# import the openai embeddings from langchain_openai
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# import the openai embeddings
from langchain_openai import OpenAIEmbeddings
# import the openai embeddings from langchain_openai
from langchain_community.vectorstores import Chroma
# Import Chatmodel
from langchain_openai import ChatOpenAI
# Import create_retrieval_chain document for retrieval with the aid of an llm 
from langchain.chains.combine_documents import create_stuff_documents_chain
# Import ConversationalRetrievalChain for doc retrieval and chatbot question answering with the aid of an llm 
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
import langchain_community.vectorstores as vectorstores
from langchain.chains.question_answering import load_qa_chain

from langchain_community.document_loaders import UnstructuredExcelLoader

loader = UnstructuredExcelLoader("contest1.xlsx", mode="elements")
docs = loader.load()

# Set the memory for the ConversationalRetrievalChain
# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True
# )

# Set the persist directory for the vector store
persist_directory = 'docs/chroma/'

# Load the .env file
_ = load_dotenv(find_dotenv()) # read local .env file

# Set the openai api key
openai.api_key  = os.environ['OPENAI_API_KEY']


# Set the openai api key
key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


chain = load_qa_chain(llm=llm,chain_type="map_reduce")
print(chain.run(input_documents=docs,question="Ask me 5 riddle questions based on the document whiles giving the clues"))


# # Create an instance of the openai embeddings
# embedding = OpenAIEmbeddings()

# # #Pdf content loading
# # loader1 = PyPDFLoader("./Acawriting.pdf")
# # pages = loader1.load()


# # Set the chunk size and overlap
# chunk_size = 1500
# chunk_overlap = 4

# # Create an instance of the recursive character text splitter
# r_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=chunk_size,
#     chunk_overlap=0,
#     separators= ['\n\n', '\n',"(?<=\. )", " ",""]
# )

# # Create an instance of the character text splitter
# c_splitter = CharacterTextSplitter(
#     chunk_size=chunk_size,
#     chunk_overlap=chunk_overlap,
#     separator=''
# )


# # Split the documents
# docss = r_splitter.split_documents(docs)

# #print(docs)
# # Store the documents in a vector store


# # Load the vector store
# vectordb = Chroma.from_documents(
#     documents=vectorstores.utils.filter_complex_metadata(docs),
#     embedding=embedding,
#     persist_directory=persist_directory
# )

# # Print the number of documents in the vector store
# print(vectordb._collection.count())

# # Set the llm

# # Create a doc retriever
# retriever=vectordb.as_retriever()

# def qa(input,context):
#     prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

#     <context>
#     {context}
#     </context>

#     Question: {input}""")

#     # Create an instance of ConversationalRetrievalChain
#     document_chain = create_stuff_documents_chain(llm, prompt)

#     answer = create_retrieval_chain(retriever,document_chain)
    
#     return answer.invoke({
#         "input":input,
#         "contex":context
#     })




# class Kofi:
#     def __init__(self):
#         pass
#     # Text completion
#     def chat_completion(self,messages,model = "gpt-3.5-turbo"):
#         response = openai.chat.completions.create(
#                 model=model,
#                 max_tokens=1500,
#                 temperature=0,
#                 messages=messages,
#             )
#         return response.choices[0].message.content

#     # Ask a question
#     def ask_question(self,question):
#         answer = qa(question,"Physics")
#         return answer['answer']

# kofi = Kofi()

# print(kofi.ask_question("Ask me some questions"))



