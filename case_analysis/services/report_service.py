class ReportService:

    def __init__(self, sf):
        self.sf = sf

    def get_report_details(self, report_id):

        endpoint = f"analytics/reports/{report_id}/describe"

        report_data = self.sf.restful(endpoint)

        return report_data