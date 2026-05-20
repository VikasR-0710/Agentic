import sys
import os

sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd

from case_analysis.clients.salesforce_connector import SalesforceConnector
from case_analysis.services.case_service import CaseService
from case_analysis.services.openai_service import OpenAIService



# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Agentic AI Leadership Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top:10px;
}

.block-container{
    padding-top:1rem;
}

h1{
    font-size:42px !important;
    font-weight:800 !important;
}

[data-testid="stHorizontalBlock"]{
gap:0.2rem;
}

p{
font-size:12px !important;
}

button{
font-size:11px !important;
padding:0.1rem !important;
}        
            
    

</style>
""",unsafe_allow_html=True)




# ---------------------------------------------------
# REGION MAP
# ---------------------------------------------------

OWNER_REGION_MAP={

"Sakthi Devi SK":"APAC",
"Mohamed Ramzin":"APAC",
"Syeda Sajida":"APAC",
"Yogesh R":"APAC",
"Ganesh Babu":"APAC",
"Naveen Kumar Surisetti":"APAC",
"Srinivas Aaguri":"APAC",

"Abhishek Bose":"EMEA",
"Sindhu M Y":"EMEA",
"Payal Gupta":"EMEA",
"Poonam Pandey":"EMEA",
"Mugilan Gowthaman":"EMEA",
"Santosh Veduruvada":"EMEA",
"Sivagnana Bharathi Nagaraj":"EMEA",
"Ullas Shenoy":"EMEA",
"Vipul SG":"EMEA",
"Vilas Potadar":"EMEA",
"Chethan Kumar P.":"EMEA",
"Amith Gujjar":"EMEA",
"Monika Sihag":"EMEA",
"Chandra Sai Surya Santosh Veduruvada":"EMEA",

"Aqsa Pandith":"NA EAST",
"Prabu R":"NA EAST",
"Vikas R":"NA EAST",
"Tarun Buthala":"NA EAST",
"Gnanasiri Pechetti":"NA EAST",
"Shivendra Yadav":"NA EAST",
"Kaushik Patowary":"NA EAST",
"Shahrukh Shahzad":"NA EAST",
"Amit Bhojak":"NA EAST",
"Mohammed Usman":"NA EAST",
"Santi Sahoo":"NA EAST",
"Nilanjan Roy":"NA EAST",
"Nupur Rao":"NA EAST",
"Rohit Nargundkar":"NA EAST",
"Prabu Rajendran":"NA EAST",
"Palak Kharche":"NA EAST",
"Pooja Singh":"NA EAST",
"Becca Lozano":"NA EAST",
"Mohammad Raza":"NA EAST",
"Sumit Paul":"NA EAST",

"Selvin Raja":"NA WEST",
"Shakti Prasad Pati":"NA WEST",
"Sanjay Kademani":"NA WEST",
"Shreyas G Nambiar":"NA WEST",
"Vishal Mavi":"NA WEST",
"Infant Raj.":"NA WEST",
"Pallavi M R":"NA WEST",
"Aniket Chinde":"NA WEST",
"Kalyan Kumar":"NA WEST",
"Amit Kumar":"NA WEST",
"Karthik Dosapati":"NA WEST",
"Peter Kyller":"NA WEST",
"Imari Killikelly":"NA WEST",
"Anthony Pham":"NA WEST",
"Sushmitha Rayalkeri":"NA WEST",
"Merlyn Pushparaj":"NA WEST",
"ZAREENA BANO":"NA WEST",
"Joshua Halle" : "NA WEST",
"Karalie Murray" : "NA WEST"
}



# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def get_region(owner):

    return OWNER_REGION_MAP.get(
        owner,
        "UNKNOWN"
    )



@st.cache_data(ttl=180)
def fetch_cases():

    connector=SalesforceConnector()

    sf=connector.connect()

    service=CaseService(sf)

    return service.get_recent_cases()



# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("Prioritisation Dashboard")

st.markdown("---")



# ---------------------------------------------------
# LOAD CASES
# ---------------------------------------------------

with st.spinner("Fetching Salesforce Cases..."):

    cases=fetch_cases()



if "sentiments" not in st.session_state:

    st.session_state.sentiments={}



dashboard=[]



for case in cases:

    if case is None:
        continue

    owner_name = (
        case.get("Owner") or {}
    ).get(
        "Name",
        "UNKNOWN"
    )

    customer_name = (
        case.get("Account") or {}
    ).get(
        "Name",
        "N/A"
    )

    support_level = (
        case.get("Support_Level__c")
        or "N/A"
    )

    escalated = (
        case.get("IsEscalated")
        or False
    )

    region = get_region(owner_name)

    dashboard.append({

        "Region": region,
        "Case Number": case.get(
            "CaseNumber",
            "N/A"
        ),

        "Customer Name": customer_name,

        "Case Owner": owner_name,

        "Support Level": support_level,

        "Status": case.get(
            "Status",
            "N/A"
        ),

        "Escalated": escalated,

        "Sentiment": st.session_state.sentiments.get(
            case.get("CaseNumber"),
            "Not Analyzed"
        )
    })


df=pd.DataFrame(dashboard)



# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

c1,c2=st.columns(2)

with c1:

    regions=sorted(
        df["Region"].unique()
    )

    selected_regions=st.multiselect(
        ":earth_africa: Region",
        regions,
        default=regions
    )

with c2:

    owners=sorted(
        df["Case Owner"].unique()
    )

    selected_owners=st.multiselect(
        ":bust_in_silhouette: Owner",
        owners,
        default=owners
    )



if not selected_regions:
    selected_regions = regions

if not selected_owners:
    selected_owners = owners



filtered_df = df[
    (df["Region"].isin(selected_regions))
    &
    (df["Case Owner"].isin(selected_owners))
]


# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

a,b,c,d=st.columns(4)

# a.metric(
# ":package: Total",
# len(filtered_df)
# )

# b.metric(
# ":rotating_light: Escalated",
# len(
# filtered_df[
# filtered_df["Escalated"]==True
# ]
# )
# )

# c.metric(
# ":earth_africa: Regions",
# filtered_df["Region"].nunique()
# )

# d.metric(
# ":bust_in_silhouette: Owners",
# filtered_df["Case Owner"].nunique()
# )

st.markdown("---")



# ---------------------------------------------------
# REPORT
# ---------------------------------------------------

left,right = st.columns([1,1])

with left:

    st.subheader(":clipboard: AI Case Monitoring")




    report_box = st.container(height=350)

    with report_box:

        openai_service = OpenAIService()
        headers = st.columns([1,1,2.5,2,1.2,1.2,1,1.5])

        headers[0].write("Region")
        headers[1].write("Case")
        headers[2].write("Customer")
        headers[3].write("Owner")
        headers[4].write("Support")
        headers[5].write("Status")
        headers[6].write("Escalated")
        headers[7].write("Sentiment")

        st.markdown("---")
        for index,row in filtered_df.iterrows():

            cols = st.columns(
                [1,1,2.5,2,1.2,1.2,1,1.5]
            )

            cols[0].write(
                row["Region"]
            )

            cols[1].write(
                row["Case Number"]
            )

            cols[2].write(
                row["Customer Name"]
            )

            cols[3].write(
                row["Case Owner"]
            )

            cols[4].write(
                row["Support Level"]
            )

            cols[5].write(
                row["Status"]
            )

            cols[6].write(
                "Yes" if row["Escalated"]
                else "No"
            )

            sentiment=row["Sentiment"]

            if sentiment=="Not Analyzed":

                if cols[7].button(
                    ":brain: Analyze",
                    key=f"analyze_{row['Case Number']}"
                ):

                    with st.spinner(
                        f"Analyzing {row['Case Number']}..."
                    ):

                        matching_case=next(
                            c for c in cases
                            if c["CaseNumber"]
                            == row["Case Number"]
                        )

                        response=openai_service.analyze_case(
                            matching_case
                        )

                        st.session_state.sentiments[
                            row["Case Number"]
                        ]=response

                        st.rerun()

            else:

                cols[7].success(
                    sentiment
                )

with right:

    st.empty()

st.markdown("---")

st.caption(
":arrows_counterclockwise: Dashboard refreshes every 3 minutes from Salesforce"
)