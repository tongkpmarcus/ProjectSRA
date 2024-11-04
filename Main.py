import os
import streamlit as st
from dotenv import load_dotenv
from helper_functions import llm
from utility import check_password

if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# region <--------- RAG config --------->

if __name__ == "__main__":
    # Path to your PDF files 
    pdf_paths = "AeMF_SRA.pdf","Common_SRA.pdf","Mock_previous_incidents.pdf"

   
    # Load the PDF
    documents = llm.load_pdf(pdf_paths)
    print(f"Total documents loaded: {len(documents)}")

    # Split and chunk the loaded documents
    splitted_documents = llm.split_chunk_text(documents)
    print(f"Total chunks created: {len(splitted_documents)}")
    print(splitted_documents)  # Inspect the structure of splitted_documents

    # Embed documents into vector store and load it
    vectordb = llm.embed_vector_store(splitted_documents)
    print("Vector store created and persisted.")
        
    # To load the vector store from disk
    vectordb = llm.load_vector_store()
    print("Vector store loaded from disk.")

    # Step 4: Set up the QA retrieval chain
    qa_chain = llm.retrieve_QA(vectordb)

# endregion <--------- RAG config --------->

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Project SRA",
    page_icon="✈️"
)
# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()
# Title and Description
st.title("Project SRA")
st.markdown(
    """
    Welcome to the Safety Risk Assessment tool! 
    Please select a flight and enter the maintenance task you want to evaluate.
    """
)

# Sidebar for Navigation (optional)
# st.sidebar.success("Select Any Page from here") 
# endregion <--------- Streamlit App Configuration --------->



# Flight Selection
st.header("Flight Selection")
flight = st.selectbox("Select Flight (This will help us narrow down the tasks)", options=["Flight A", "Flight B", "Flight C"])

# Form for User Input
st.header("Enter Task")
form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Describe the aircraft maintenance task:", height=100)

# Submit Button
if form.form_submit_button("Submit"):
    st.success("Your input has been submitted!")
    
    # Prepare the prompt for the LLM
    prompt = f"""
    The prompt below should be an aircraft maintenance task. If it does not sound like one, respond with "Please enter a valid task.".\n
    Find the closest Incident report to the task from Mock_previous_incidents, if not related, put NIL, do not hallucinate, only take in incidents from mock_incident_report. 
    If valid, use qachain to help answer and provide a response in the following format:

    Equipment Needed:
    Hazards:
    Consequences:
    Control Measures:

    Other Suggestions and Tips:

    Previous Incident Reports:

    Text: '''{user_prompt}'''

   
    """
    


    # Get the response from the language model
    response = llm.get_completion(prompt)

    # Call `llm_answer` with the `qa_chain`
    response_emb = llm.llm_answer(prompt, qa_chain)
    
    # Display the response in a code block for better formatting
    #st.markdown("### Response:")
    #st.write(response)
    #st.markdown("### Response_emb:")
    #st.write(response_emb)
    #print(f"User Input is {user_prompt}")

    col1, col2= st.columns(2)

    with col1:
        st.header("Response:")
        st.write(response)

    with col2:
        st.header("Response_emb:")
        st.write(response_emb)

with st.expander(
    """IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. 
    The information provided here is NOT intended for actual usage and should not be relied upon 
    for making any decisions, especially those related to financial, legal, or healthcare matters."""
)







