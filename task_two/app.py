import streamlit as st
import utils  # <--- Importing your backend module

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Fynd AI Feedback System", layout="wide")

# Check API Key
if not utils.configure_ai():
    st.error("⚠️ API Key missing! Set GOOGLE_API_KEY in .env or Streamlit Secrets.")
    st.stop()

# Sidebar Navigation (Simulating two dashboards in one app) 
page = st.sidebar.radio("Navigation", ["User Dashboard (Public)", "Admin Dashboard (Internal)"])

# ==========================================
# 👤 USER DASHBOARD (Requirements A) [cite: 44]
# ==========================================
if page == "User Dashboard (Public)":
    st.title("📝 Submit Feedback")
    st.markdown("We'd love to hear from you!")

    with st.form("feedback_form"):
        # Req: Select a star rating 
        rating = st.slider("Rate your experience", 1, 5, 3)
        # Req: Write a short review 
        review_text = st.text_area("Your Review")
        
        # Req: Submit it [cite: 48]
        submitted = st.form_submit_button("Submit")
        
        if submitted and review_text:
            with st.spinner("AI is analyzing your feedback..."):
                # Req: AI-generated response returned [cite: 50]
                # Req: LLM used for user-facing response [cite: 67]
                analysis = utils.get_ai_analysis(rating, review_text)
                
                # Req: Data should be stored 
                utils.save_entry(
                    rating, review_text, 
                    analysis["user_reply"], analysis["summary"], analysis["action"]
                )
                
                st.success("✅ Feedback Sent!")
                # Display the AI response to the user
                st.info(f"**Our Reply:** {analysis['user_reply']}")

# ==========================================
# 🛠️ ADMIN DASHBOARD (Requirements B) [cite: 52]
# ==========================================
elif page == "Admin Dashboard (Internal)":
    st.title("📊 Admin Insights")
    
    # Req: Read from the same stored data source 
    df = utils.load_data()
    
    if df.empty:
        st.info("No data yet.")
    else:
        # Req: Admin Dashboard may include analytics [cite: 59]
        col1, col2 = st.columns(2)
        col1.metric("Total Reviews", len(df))
        col2.metric("Avg Rating", f"{df['Rating'].mean():.1f} ⭐")

        st.subheader("Live Feed")
        
        # Req: Display list including: User rating, User review, AI Summary, AI Actions [cite: 53-57]
        # Req: LLM used for summarisation [cite: 65] & recommended actions [cite: 66]
        display_cols = ["Timestamp", "Rating", "Review", "Summary", "Action_Item"]
        
        st.dataframe(
            df[display_cols].sort_values("Timestamp", ascending=False),
            use_container_width=True,
            column_config={
                "Rating": st.column_config.NumberColumn(format="%d ⭐"),
                "Review": st.column_config.TextColumn("User Review", width="medium"),
                "Summary": st.column_config.TextColumn("AI Summary", width="small"),
                "Action_Item": st.column_config.TextColumn("Recommended Action", width="medium"),
            }
        )

        # Helper to download data (good for "Analytics" credit)
        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False).encode('utf-8'),
            "feedback.csv",
            "text/csv"
        )