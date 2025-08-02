import pandas as pd
from flask import Flask, jsonify, render_template
import os

# Initialize the Flask application
app = Flask(__name__)

# Define the path to your CSV file
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'Data Perjawatan JKN Johor.csv')

def get_marker_data():
    """
    Reads the CSV, processes it, and returns a list of dictionaries
    suitable for allMarkersData in JavaScript.
    """
    try:
        # Read the CSV with a multi-level header to correctly capture all headers
        df = pd.read_csv(CSV_FILE_PATH, header=[3, 4])

        markers_data = []

        # Get the column names from the multi-level header
        name_col = df.columns[1]
        lat_col = df.columns[2]
        lng_col = df.columns[3]

        # These columns are part of the multi-level header, so we access them by their tuple index
        j_col = df.columns[4]
        i_col = df.columns[5]
        k_col = df.columns[6]

        for index, row in df.iterrows():
            location_name = row[name_col]

            # Skip empty or summary rows
            if pd.isna(location_name) or 'RINGKASAN' in str(location_name) or 'TOTAL' in str(location_name) or 'JABATAN' in str(location_name):
                continue

            location_name = str(location_name).strip()
            
            # --- Placeholder logic for url, description, and category ---
            # You can customize this logic based on your needs.
            url = f"pages/{location_name.replace(' ', '_').lower()}.html"
            description = f"Public health facility: {location_name}."
            
            if "HOSPITAL" in location_name.upper():
                category = "Hospital"
            elif "KLINIK" in location_name.upper():
                category = "Clinic"
            else:
                category = "Other"
            
            # --- End of placeholder logic ---

            # Check if lat and lng are valid before adding to the list
            if pd.notna(row[lat_col]) and pd.notna(row[lng_col]):
                markers_data.append({
                    "name": location_name,
                    "lat": row[lat_col],
                    "lng": row[lng_col],
                    "url": url,
                    "description": description,
                    "category": category,
                    "J": row[j_col],
                    "I": row[i_col],
                    "K": row[k_col]
                })
        return markers_data

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
        return []
    except Exception as e:
        print(f"An error occurred while processing CSV: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/markers')
def markers_api():
    data = get_marker_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
