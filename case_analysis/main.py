import time

from case_analysis.clients.salesforce_connector import SalesforceConnector
from case_analysis.services.case_service import CaseService
from case_analysis.services.openai_service import OpenAIService
from case_analysis.services.geminiai_service import GeminiService



def main():

    connector = SalesforceConnector()

    sf = connector.connect()

    case_service = CaseService(sf)

    openai_service = OpenAIService()

    gemini_service = GeminiService()

    cases = case_service.get_recent_cases()

    print("\nRecent Cases:\n")

    for case in cases:

        print(f"""
Case Number : {case['CaseNumber']}
Subject     : {case['Subject']}
Status      : {case['Status']}
        """)

        print("\nOPENAI ANALYSIS:\n")

        openai_analysis = openai_service.analyze_case(case)

        print(openai_analysis)

        print("\n" + "-" * 70)

        print("\nGEMINI ANALYSIS:\n")

        gemini_analysis = gemini_service.analyze_case(case)
        time.sleep(12)

        print(gemini_analysis)

        print("\n" + "=" * 70)



if __name__ == "__main__":
    main()