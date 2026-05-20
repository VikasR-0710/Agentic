import sys
import os

# This adds the root directory (AI folder) to your Python path
sys.path.append(os.getcwd())

import streamlit as st
import time
from case_analysis.clients.salesforce_connector import SalesforceConnector
from case_analysis.services.case_service import CaseService
from case_analysis.services.openai_service import OpenAIService
from case_analysis.services.geminiai_service import GeminiService

def newmain():
    st.set_page_config(page_title="Salesforce Case Analyzer", layout="wide")
    st.title(":bar_chart: Salesforce Case Analysis Dashboard")

    # Initialize Services
    @st.cache_resource
    def init_services():
        connector = SalesforceConnector()
        sf = connector.connect()
        return CaseService(sf), OpenAIService(), GeminiService()

    case_service, openai_service, gemini_service = init_services()

    if st.button('Fetch and Analyze Cases'):
        with st.spinner('Fetching cases from Salesforce...'):
            cases = case_service.get_recent_cases()

        for case in cases:
            with st.container():
                st.markdown(f"### Case: {case['CaseNumber']}")

                # Layout columns for Case Details
                col1, col2, col3 = st.columns(3)
                col1.metric("Status", case['Status'])
                col2.metric("Owner", case['Owner']['Name'])
                col3.write(f"**Subject:** {case['Subject']}")

                # Analysis Tabs
                tab1, tab2 = st.tabs(["OpenAI Analysis", "Gemini Analysis"])

                with tab1:
                    with st.spinner('Analyzing with OpenAI...'):
                        openai_analysis = openai_service.analyze_case(case)
                        st.info(openai_analysis)

                with tab2:
                    # Uncommenting your Gemini logic
                    with st.spinner('Analyzing with Gemini...'):
                        # gemini_analysis = gemini_service.analyze_case(case)
                        # st.success(gemini_analysis)
                        st.write("Gemini Analysis is currently disabled in script.")

                st.divider()

if __name__ == "__main__":
    newmain()