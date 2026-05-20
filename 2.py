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
""", unsafe_allow_html=True)


# ---------------------------------------------------
# REGION MAP
# ---------------------------------------------------

OWNER_REGION_MAP={
    "Sakthi Devi SK":"APAC", "Mohamed Ramzin":"APAC", "Syeda Sajida":"APAC", 
    "Yogesh R":"APAC", "Ganesh Babu":"APAC", "Naveen Kumar Surisetti":"APAC", 
    "Srinivas Aaguri":"APAC",
    "Abhishek Bose":"EMEA", "Sindhu M Y":"EMEA", "Payal Gupta":"EMEA", 
    "Poonam Pandey":"EMEA", "Mugilan Gowthaman":"EMEA", "Santosh Veduruvada":"EMEA", 
    "Sivagnana Bharathi Nagaraj":"EMEA", "Ullas Shenoy":"EMEA", "Vipul SG":"EMEA", 
    "Vilas Potadar":"EMEA", "Chethan Kumar P.":"EMEA", "Amith Gujjar":"EMEA", 
    "Monika Sihag":"EMEA", "Chandra Sai Surya Santosh Veduruvada":"EMEA",
    "Aqsa Pandith":"NA EAST", "Prabu R":"NA EAST", "Vikas R":"NA EAST", 
    "Tarun Buthala":"NA EAST", "Gnanasiri Pechetti":"NA EAST", "Shivendra Yadav":"NA EAST", 
    "Kaushik Patowary":"NA EAST", "Shahrukh Shahzad":"NA EAST", "Amit Bhojak":"NA EAST", 
    "Mohammed Usman":"NA EAST", "Santi Sahoo":"NA EAST", "Nilanjan Roy":"NA EAST", 
    "Nupur Rao":"NA EAST", "Rohit Nargundkar":"NA EAST", "Prabu Rajendran":"NA EAST", 
    "Palak Kharche":"NA EAST", "Pooja Singh":"NA EAST", "Becca Lozano":"NA EAST", 
    "Mohammad Raza":"NA EAST", "Sumit Paul":"NA EAST",
    "Selvin Raja":"NA WEST", "Shakti Prasad Pati":"NA WEST", "Sanjay Kademani":"NA WEST", 
    "Shreyas G Nambiar":"NA WEST", "Vishal Mavi":"NA WEST", "Infant Raj.":"NA WEST", 
    "Pallavi M R":"NA WEST", "Aniket Chinde":"NA WEST", "Kalyan Kumar":"NA WEST", 
    "Amit Kumar":"NA WEST", "Karthik Dosapati":"NA WEST", "Peter Kyller":"NA WEST", 
    "Imari Killikelly":"NA WEST", "Anthony Pham":"NA WEST", "Sushmitha Rayalkeri":"NA WEST", 
    "Merlyn Pushparaj":"NA WEST", "ZAREENA BANO":"NA WEST", "Joshua Halle" : "NA WEST", 
    "Karalie Murray" : "NA WEST"
}


# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def get_region(owner):
    return OWNER_REGION_MAP.get(owner, "UNKNOWN")

def get_priority_tier(support_level, is_escalated):
    """
    Calculates the base tier for sorting. 1 is highest priority.
    """
    score_map = {
        "SevOne": 10,
        "S1 Premium": 8,
        "Premium Plus": 8,
        "Premium (24x7)": 7, 
        "S2 Premium": 7,
        "Premium": 7,       
        "S1 Standard": 6,
        "S2 Standard": 5,
        "Standard": 5,      
        "S3 Premium": 4,
        "S4 Premium": 3,
        "S3 Standard": 2,
        "S4 Standard": 1
    }
    
    base_score = score_map.get(support_level, 0)
    escalated_score = 9 if is_escalated else 0
    
    final_score = max(base_score, escalated_score)
    
    return 11 if final_score == 0 else 11 - final_score

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

    owner_name = (case.get("Owner") or {}).get("Name", "UNKNOWN")
    customer_name = (case.get("Account") or {}).get("Name", "N/A")
    support_level = case.get("Support_Level__c") or "N/A"
    escalated = case.get("IsEscalated") or False
    region = get_region(owner_name)

    dashboard.append({
        "Region": region,
        "Case Number": case.get("CaseNumber", "N/A"),
        "Customer Name": customer_name,
        "Case Owner": owner_name,
        "Support Level": support_level,
        "Status": case.get("Status", "N/A"),
        "Escalated": escalated,
        "Sentiment": st.session_state.sentiments.get(case.get("CaseNumber"), "Not Analyzed"),
        "Priority_Tier": get_priority_tier(support_level, escalated) 
    })

df=pd.DataFrame(dashboard)


# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

c1,c2=st.columns(2)

with c1:
    regions=sorted(df["Region"].unique())
    selected_regions=st.multiselect(
        ":earth_africa: Region",
        regions,
        default=regions
    )

with c2:
    owners=sorted(df["Case Owner"].unique())
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
    (df["Region"].isin(selected_regions)) &
    (df["Case Owner"].isin(selected_owners))
]


# ---------------------------------------------------
# SORTING & PER-OWNER SEQUENTIAL RANKING
# ---------------------------------------------------

# 1. Sort by Case Owner first 
# 2. Priority_Tier (Highest priority first)
# 3. Tie-breaker: Case Number 
filtered_df = filtered_df.sort_values(by=["Case Owner", "Priority_Tier", "Case Number"], ascending=[True, True, True])

# Assign a sequential absolute rank 1, 2, 3... PER OWNER
filtered_df["Sequential_Rank"] = filtered_df.groupby("Case Owner").cumcount() + 1


# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

st.markdown("---")


# ---------------------------------------------------
# REPORT
# ---------------------------------------------------

left, right = st.columns([1,1])

with left:
    st.subheader(":clipboard: AI Case Monitoring")

    report_box = st.container(height=350)

    with report_box:
        openai_service = OpenAIService()
        
        headers = st.columns([1, 1, 2.5, 2, 1.2, 1.2, 1, 1.5, 0.8])

        headers[0].write("**Region**")
        headers[1].write("**Case**")
        headers[2].write("**Customer**")
        headers[3].write("**Owner**")
        headers[4].write("**Support**")
        headers[5].write("**Status**")
        headers[6].write("**Escalated**")
        headers[7].write("**Sentiment**")
        headers[8].write("**Rank**")

        st.markdown("---")
        
        for index, row in filtered_df.iterrows():
            cols = st.columns([1, 1, 2.5, 2, 1.2, 1.2, 1, 1.5, 0.8])

            cols[0].write(row["Region"])
            cols[1].write(row["Case Number"])
            cols[2].write(row["Customer Name"])
            cols[3].write(row["Case Owner"])
            cols[4].write(row["Support Level"])
            cols[5].write(row["Status"])
            cols[6].write("Yes" if row["Escalated"] else "No")

            sentiment = row["Sentiment"]

            if sentiment == "Not Analyzed":
                if cols[7].button(":brain: Analyze", key=f"analyze_{row['Case Number']}"):
                    with st.spinner(f"Analyzing {row['Case Number']}..."):
                        matching_case = next(
                            c for c in cases
                            if c["CaseNumber"] == row["Case Number"]
                        )
                        response = openai_service.analyze_case(matching_case)
                        st.session_state.sentiments[row["Case Number"]] = response
                        st.rerun()
            else:
                # DYNAMIC SENTIMENT COLORS
                sentiment_lower = sentiment.lower()
                
                if "positive" in sentiment_lower:
                    cols[7].success(sentiment) # Green
                elif "medium" in sentiment_lower or "neutral" in sentiment_lower:
                    cols[7].warning(sentiment) # Yellow
                elif "negative" in sentiment_lower or "critical" in sentiment_lower:
                    cols[7].error(sentiment)   # Red
                else:
                    cols[7].info(sentiment)    # Blue fallback for any other string

            # Display the PER-USER sequential rank
            cols[8].write(str(row["Sequential_Rank"]))

with right:
    st.empty()

st.markdown("---")

st.caption(
":arrows_counterclockwise: Dashboard refreshes every 3 minutes from Salesforce"
)