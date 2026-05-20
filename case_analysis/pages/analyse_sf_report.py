from case_analysis.clients.salesforce_connector import SalesforceConnector
from case_analysis.services.report_service import ReportService



def main():

    connector = SalesforceConnector()

    sf = connector.connect()

    report_service = ReportService(sf)

    # Replace with your report ID
    report_id = "00ORi00000MO7IDMA1"

    report_details = report_service.get_report_details(report_id)

    print("\n==============================")
    print("REPORT DETAILS")
    print("==============================\n")

    # REPORT NAME
    print("REPORT NAME:")
    print(report_details["reportMetadata"]["name"])

    print("\n==============================")

    # REPORT TYPE
    print("\nREPORT TYPE:")
    print(report_details["reportMetadata"]["reportType"])

    print("\n==============================")

    # REPORT ID
    print("\nREPORT ID:")
    print(report_id)

    print("\n==============================")

    # COLUMNS
    print("\nCOLUMNS:\n")

    columns = report_details["reportMetadata"]["detailColumns"]

    for column in columns:
        print(column)

    print("\n==============================")

    # FILTERS
    print("\nFILTERS:\n")

    filters = report_details["reportMetadata"].get(
        "reportFilters",
        []
    )

    for filter_data in filters:
        print(filter_data)

    print("\n==============================")

    # STANDARD FILTER
    print("\nSTANDARD FILTER:\n")

    standard_filters = report_details["reportMetadata"].get(
        "standardDateFilter",
        {}
    )

    print(standard_filters)

    print("\n==============================")

    # GROUPINGS DOWN
    print("\nGROUPINGS DOWN:\n")

    groupings_down = report_details.get(
        "groupingsDown",
        {}
    )

    print(groupings_down)

    print("\n==============================")

    # GROUPINGS ACROSS
    print("\nGROUPINGS ACROSS:\n")

    groupings_across = report_details.get(
        "groupingsAcross",
        {}
    )

    print(groupings_across)

    print("\n==============================")

    # AGGREGATES
    print("\nAGGREGATE COLUMNS:\n")

    aggregates = report_details["reportMetadata"].get(
        "aggregates",
        []
    )

    for aggregate in aggregates:
        print(aggregate)

    print("\n==============================")

    # FULL RAW JSON
    print("\nFULL REPORT JSON:\n")

    print(report_details)



if __name__ == "__main__":
    main()