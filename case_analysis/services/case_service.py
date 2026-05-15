class CaseService:

    def __init__(self, sf_client):
        self.sf = sf_client

    def get_recent_cases(self):

        query = """
        SELECT Id, CaseNumber, Subject, Status
        FROM Case
        LIMIT 5
        """

        result = self.sf.query(query)

        return result["records"]