import streamlit as st
import requests

# Flask API endpoint
API_URL = "http://127.0.0.1:5000/recommend"  # Update this if your Flask server is hosted elsewhere

def query_flask_api(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            return response.json().get("recommended_assessments", [])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Exception: {str(e)}")
        return []

def main():
    st.title("SHL Assessment Assistant")
    st.markdown("*Ask questions about the SHL assessment documents.*")

    query = st.text_input("Enter your query:")

    if st.button("Search"):
        if not query:
            st.error("Please enter a query!")
        else:
            results = query_flask_api(query)
            if results:
                st.write("### Recommended Assessments")
                for i, result in enumerate(results, start=1):
                    st.write(f"**Result {i}:**")
                    st.write(f"**URL:** {result['url']}")
                    st.write(f"**Adaptive Support:** {result['adaptive_support']}")
                    st.write(f"**Description:** {result['description']}")
                    st.write(f"**Duration:** {result['duration']} minutes")
                    st.write(f"**Remote Support:** {result['remote_support']}")
                    st.write(f"**Test Type:** {', '.join(result['test_type'])}")
                    st.write("---")
            else:
                st.write("No recommendations found.")

if __name__ == "__main__":
    main()
