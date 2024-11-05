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
    - Helping our Air Force Engineers conduct their before action review and safety risk assessment
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
    To form our project, we rely on diverse data sources, including:  
    - Common SRA: This document consists of the general tasks that Air Force Engineers may encounter during their time at work. Ranging from towing equipment to the use of POL, this SRA will state the hazards and risks involved in various tasks.  
    - Flight SRA: By utilizing existing information on various flights and their respective tasks, we can extract individual tasks according to their specific maintenance flight. In this document, aspects such as control measures, PPE, and hazards will be listed.  
    - Incident reports: Past incidents that have occurred to others. The report will briefly explain the main events that led to the accident or problem. It will serve as a cautionary warning and remind the user of what can happen with that particular task.


    """
)

st.title("Key Features") 
st.markdown(
    """
    Project SRA (ProSRA) offers a range of features designed to enhance your experience:  
    - Centralized information:** All information will be organized on one page according to its categories. No more cross-referencing between the flight SRA and common SRA will be required. You can forget about scrolling through the PDF manually to find the information you need.  
    - Past lessons learned:** Some additional features that will be beneficial include the incorporation of incident reports. These will serve as pointers from people’s experiences, highlighting certain aspects that may not be stated in the SRA.

    """
)

st.sidebar.success("You are currently viewing About Us")
