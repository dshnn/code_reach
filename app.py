import streamlit as st
from pipeline import pipeline
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="CodeReach",
    page_icon="🚀",
    layout="wide"
)

# ---------------- Hero Section ---------------- #

st.title("🚀 CodeReach")

st.markdown("""
🚀 CodeReach

Turn company websites into interview opportunities.

Paste any company website below.
We'll analyze it, suggest projects you can build,
and generate a personalized cold email.
""")

st.divider()

# ---------------- Input ---------------- #

url = st.text_input(
    "🔗 Company Website",
    placeholder="https://company.com"
)

generate = st.button(
    "🚀 Generate Pitch",
    use_container_width=True
)

# ---------------- Pipeline ---------------- #

if generate:

    with st.spinner("Analyzing Website..."):

        result = pipeline(url)

    if not result["status"]:

        st.error(f"❌ {result['stage']} Failed, Kindly check your terminal console for more information")

        st.code(result["error"])

        st.stop()

    result = result["data"]

    st.success("Analysis Complete!")

    st.subheader("📧 Contact Email")
    st.code(result["email"])

    st.subheader("📬 Subject Lines")
    for subject in result["subject_lines"]:
        st.markdown(f"- {subject}")

    st.subheader("✉️ Cold Email")
    st.text_area("", result["email_body"], height=260)

    st.subheader("🔁 Follow-up")
    st.text_area("", result["follow_up_email"], height=220)


st.divider()

st.caption(
    "Built with ❤️ using Gemini • BeautifulSoup • Streamlit"
)



