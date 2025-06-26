
import streamlit as st
from workflow.workflow import RERAScrapper, main
import time

class RERAScraperApp:
    def __init__(self):
        """Initialize the scraper app."""
        self.city = None
        self.headless_mode = True

    def render_title(self):
        """Display the title and description."""
        st.title("🤖 Welcome to Karnataka RERA Scraper")
        st.write("Enter the city name and click the Scrape button to fetch data.")
        st.markdown(
                "[RERA JSON Data Sheet](https://docs.google.com/spreadsheets/d/1lnVDiO3xTA43cIDGd5OEoxC2P1hFFpM9L5BQw2AIxUs/edit?gid=81977438#gid=81977438)"
            )

    def render_inputs(self):
        """Render input fields for user interaction."""
        # City Selection
        self.city = st.selectbox(
            "Select a City",
            [
            "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", 
            "Bidar", "Chamarajanagar", "Chikkaballapura", "Chikkamagaluru", 
            "Chitradurga", "Dakshina Kannada", "Davangere", "Dharwad", "Gadag", 
            "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", 
            "Mysore", "Raichur", "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", 
            "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir"
        ],
            index=0  # Default selection
        )

        # Scraper Mode Selection
        mode = st.radio(
            "Select Scraper Mode",
            ("Headless", "With GUI"),
            index=0  # Default to Headless
        )
        self.headless_mode = mode == "Headless"

        # Display Selected City
        st.write(f"You selected: {self.city}")

    def scrape(self):
        """Trigger the scraping process."""
        if self.city:
            try:
                st.info("Initializing scraper...")
                main(self.city, self.headless_mode)
                st.success("Scraping completed successfully!")
            except Exception as e:
                st.error(f"An error occurred during scraping: {str(e)}")
        else:
            st.warning("Please select a city before starting the scraper.")

    def render_button(self):
        """Render the scrape button."""
        if st.button("Scrape"):
            self.scrape()

    def run(self):
        """Run the Streamlit app."""
        self.render_title()
        self.render_inputs()
        self.render_button()

# Create an instance of the app and run it
if __name__ == "__main__":
    app = RERAScraperApp()
    app.run()
