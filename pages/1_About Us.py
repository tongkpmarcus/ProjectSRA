import streamlit as st
st.set_page_config(
    layout="centered",
    page_title="Project SRA",
    page_icon="✈️"
)
st.title("About Us") 
st.markdown(
    """
    Welcome to Project SRA(ProSRA), where we are dedicated to simplifying safety risk assessments for everyone.
    Our mission is to make the reviewing process efficient and straightforward, 
    empowering everyone to identify and manage risks with confidence and ease. 
    By streamlining previous cross-examining processes for risk assessment, 
    we now provide a user-friendly interface that lists all necessary information for SRA, 
    all in one place. 

    """
)
st.title("Project Scope") 
st.markdown(
    """
    Our project focuses on:
    -  Helping our Air Force Engineers conduct their before action review and safety risk assessment
    - Reducing the amount of time needed for reviewing the risk assessment
    - Collating the common SRA, flight SRA and other relevant documents into one platform  
    """
)
st.title("Objectives") 
st.markdown(
    """
    We strive to achieve the following objectives:
    
    1. Ability to select flight SRA: You will be able to search your specific flight SRA via the drop down list.
    2. Ability to type in task into search function: Search the task you need within seconds.
    3. Ability to easily view important information: All the information you need will be listed according to their category. 

    """
)

st.title("Data Sources") 
st.markdown(
    """
    To inform our project, we rely on diverse data sources, including:
    - Common SRA: Gathering insights through [describe methods like surveys, interviews, etc.].
    - Flight SRA: Utilizing existing research and reports from [list specific sources].
    """
)

st.title("Key Features") 
st.markdown(
    """
    Project SRA (ProSRA) offers a range of features designed to enhance your experience:
    - Past lessons learnt: Some additional features that will be beneficial are the inclusion of FAIRs, GAIRs & past lessons learnt. These will serve as pointers from people’s experiences, to take note of certain things that may not be stated in the SRA. 
    - All information accessed on one platform: All information will be organized on one page, according to their categories. No more cross referring to the flight SRA and common SRA will be required. You can forget about scrolling through the PDF manually and finding the information you need. 

    """
)

st.sidebar.success("You are currently viewing About Us")
