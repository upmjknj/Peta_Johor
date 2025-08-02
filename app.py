import pandas as pd
from flask import Flask, jsonify, render_template
import os

# Initialize the Flask application
app = Flask(__name__)

# Define the path to your CSV file
# This ensures that the Flask app can find your CSV file no matter where you run the script from.
# It joins the directory of the current file (app.py) with the name of your CSV file.
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'Data Perjawatan JKN Johor.csv') 

def get_marker_data():
    """
    Reads the CSV, processes it, and returns a list of dictionaries
    suitable for allMarkersData in JavaScript.
    """
    try:
        # Read the CSV file using pandas.
        # 'header=3' is crucial here because your CSV file has 3 lines of introductory text
        # before the actual column headers (Bil, JABATAN / BAHAGIAN / HOSPITAL / PKD / PPD, etc.) 
        df = pd.read_csv(CSV_FILE_PATH, header=3) # 

        # Initialize an empty list to store the processed marker data
        markers_data = []

        # Iterate through each row of the DataFrame
        for index, row in df.iterrows():
            # Extract the location name from the second column (index 1) 
            location_name = row.iloc[1]

            # Skip rows that are empty, contain 'TOTAL', 'BAHAGIAN', 'RINGKASAN',
            # or the main 'JABATAN KESIHATAN NEGERI JOHOR' heading,
            # as these are summary or general entries, not specific markers. 
            if pd.isna(location_name) or \
               "TOTAL" in str(location_name).upper() or \
               "BAHAGIAN" in str(location_name).upper() or \
               "RINGKASAN" in str(location_name).upper() or \
               "JABATAN KESIHATAN NEGERI JOHOR" == str(location_name).strip().upper():
                continue

            # Clean up the location name to create a URL-friendly string.
            # Convert to lowercase, replace spaces and slashes with underscores, and remove double underscores.
            if isinstance(location_name, str):
                cleaned_name = location_name.strip().lower().replace(' ', '_').replace('/', '_').replace('__', '_')
                url = f"pages/{cleaned_name}.html"
            else:
                url = "#" # Fallback if location_name is not a string

            # Extract the 'J', 'I', and 'K' values from the CSV.
            # Based on the CSV structure:
            # - `J` value: corresponds to 'Jawatan Sebenar (Tetap)' which is column 3 (index 3) 
            # - `I` value: corresponds to the first 'J' column (unnamed) which is column 4 (index 4) 
            # - `K` value: corresponds to the 'I' column (unnamed) which is column 5 (index 5) 
            # `pd.to_numeric` converts values to numbers, and `errors='coerce'` turns non-numeric into NaN.
            # `fillna(0)` then replaces any NaN values with 0.
            j_val = pd.to_numeric(row.iloc[4], errors='coerce').fillna(0) # Corrected index for 'Jawatan Sebenar (Tetap)'
            i_val = pd.to_numeric(row.iloc[6], errors='coerce').fillna(0) # Corrected index for 'J'
            k_val = pd.to_numeric(row.iloc[7], errors='coerce').fillna(0) # Corrected index for 'I'

            # --- IMPORTANT: Placeholder for Latitude and Longitude (lat, lng) ---
            # Your CSV file does NOT contain latitude and longitude data. 
            # You MUST replace these dummy values with actual geographic coordinates
            # for each location.
            # For demonstration, these values just create a slightly offset position for each marker.
            lat = 1.4 + (index * 0.001) # Dummy latitude, please replace with actual data
            lng = 103.7 + (index * 0.001) # Dummy longitude, please replace with actual data

            # Basic description and category assignment based on location name
            description = f"Data for {location_name}"
            category = "General"
            if "HOSPITAL" in str(location_name).upper():
                category = "Hospital"
            elif "PEJABAT KESIHATAN DAERAH" in str(location_name).upper() or "PKD" in str(location_name).upper():
                category = "PKD"
            elif "PEJABAT PERGIGIAN DAERAH" in str(location_name).upper() or "PPD" in str(location_name).upper():
                category = "PPD"
            elif "BAHAGIAN" in str(location_name).upper() or "IBU PEJABAT" in str(location_name).upper():
                category = "Headquarters/Division"

            # Append the processed data as a dictionary to the list
            markers_data.append({
                "name": str(location_name).strip(),
                "lat": lat,
                "lng": lng,
                "JS": "Jawatan Sebenar (Tetap)", # Label for the first value
                "J": int(j_val), # Convert to integer for display
                "I": int(i_val), # Convert to integer for display
                "K": int(k_val), # Convert to integer for display
                "url": url,
                "description": description,
                "category": category
            })
        return markers_data

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
        return [] # Return an empty list if the file is not found
    except Exception as e:
        print(f"An error occurred while processing CSV: {e}")
        return [] # Return an empty list on other errors

@app.route('/')
def index():
    """
    This route handles requests to the root URL (e.g., http://127.0.0.1:5000/).
    It renders and sends the 'index.html' file from the 'templates' directory to the browser.
    """
    return render_template('index.html')

@app.route('/api/markers')
def markers_api():
    """
    This route defines an API endpoint (e.g., http://127.0.0.1:5000/api/markers).
    When accessed, it calls the 'get_marker_data' function to get the processed data
    and then converts that data into a JSON response to be sent to the browser.
    """
    data = get_marker_data()
    return jsonify(data)

# This block ensures that the Flask development server only runs when the script
# is executed directly (not when imported as a module).
if __name__ == '__main__':
    # 'debug=True' is great for development:
    # - It provides detailed error messages in the browser.
    # - It automatically reloads the server when you make changes to your Python code.
    # NEVER use debug=True in a production environment.
    app.run(debug=True)
