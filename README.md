# 🎬 Kiarostami Short Film Festival Dashboard

This project is an interactive dashboard that visualizes and analyzes data from the Kiarostami Short Film Festival. The goal is to provide key insights and statistics about participants, movies, and other aspects of the festival.

---

## 📊 Features

### The dashboard includes:
1. **Total Participants and Total Movies**: The number of people who participated in the festival and The total number of movies submitted.
   ![Total Participants](Screenshot%202025-02-13%20at%2023.33.38.png)
2. **Gender Breakdown**: A pie chart showing the gender distribution of participants.
   ![Gender Breakdown](newplot%20(9).png)
4. **Age Distribution**: A histogram displaying the age range of participants.
   ![Age Distribution](newplot%20(10).png)
5. **Inspired by Kiarostami**: Analysis of how many movies were inspired by Kiarostami.
   ![Inspired by Kiarostami](newplot%20(11).png)
6. **Number of Countries**: A count of participating countries, with a table showing country-specific data.
   ![Number_of_countries](Screenshot%202025-02-13%20at%2023.34.26.png)
   **Countries and Number of Movies:**
   ![Countries Represented](Screenshot%2025-02-13%at%23.34.45.png)
8. **Genre and Rejection Status**: A bar chart of movies categorized by genre and acceptance/rejection status.
   ![Genre and Rejection Status](newplot%20(12).png)
9. **Film Duration**: A histogram showing the distribution of film durations.
   ![Film Duration](newplot%20(14).png)
8. **Relation Between Inspired by Kiarostami and Rejection**:
   - Movies inspired by Kiarostami had higher acceptance rates.
   - Non-inspired movies faced more rejections.
   ![Rejection_and_Inspiration](newplot%20(13).png)

---

## 🚀 How to Use

1. **Run the Dashboard**:
   - The project is built with Dash and Python.
   - Execute the code and view the dashboard in your browser.
2. **Interact with the Dashboard**:
   - Use **sliders** to filter data by production year.
   - Use **dropdowns** to select genres or rejection statuses.

---

## 📂 Project Structure

- **`Dashboard copy.ipynb`**: The main file containing the dashboard code.
- **`data/Final_Final2.csv`**: The dataset used for analysis.
- **Visualizations**: Example charts that showcase the analysis results.

---

## 🛠️ Requirements

To run this project, you need:
- Python 3.7 or higher
- Required libraries:
  - Dash
  - Plotly
  - Pandas

Install the dependencies using:
```bash
pip install -r requirements.txt
