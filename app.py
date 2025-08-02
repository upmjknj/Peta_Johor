def get_marker_data():
    try:
        df = pd.read_csv(CSV_FILE_PATH, header=3)
        print(f"CSV Loaded. First 5 rows of data:\n{df.head()}") # See initial data
        markers_data = []

        for index, row in df.iterrows():
            location_name = row.iloc[1]
            print(f"\nProcessing row {index}: Location Name = '{location_name}'")

            if pd.isna(location_name) or \
               "TOTAL" in str(location_name).upper() or \
               "BAHAGIAN" in str(location_name).upper() or \
               "RINGKASAN" in str(location_name).upper() or \
               "JABATAN KESIHATAN NEGERI JOHOR" == str(location_name).strip().upper():
                print(f"  Skipping row {index} due to filter: '{location_name}'")
                continue

            # IMPORTANT: Verify these indices (2 and 3) match where Lat/Lng are in your CSV
            lat_val = row.iloc[2]
            lng_val = row.iloc[3]
            print(f"  Raw Lat: '{lat_val}', Raw Lng: '{lng_val}' (from CSV index 2, 3)")

            lat = pd.to_numeric(lat_val, errors='coerce').fillna(0)
            lng = pd.to_numeric(lng_val, errors='coerce').fillna(0)
            print(f"  Converted Lat: {lat}, Converted Lng: {lng}")

            if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)) or pd.isna(lat) or pd.isna(lng):
                print(f"  Skipping marker for {location_name} due to invalid coordinates AFTER CONVERSION.")
                continue

            # IMPORTANT: Verify these indices (4, 6, 7) match your J, I, K data
            j_val = pd.to_numeric(row.iloc[4], errors='coerce').fillna(0)
            i_val = pd.to_numeric(row.iloc[6], errors='coerce').fillna(0)
            k_val = pd.to_numeric(row.iloc[7], errors='coerce').fillna(0)
            print(f"  J: {j_val}, I: {i_val}, K: {k_val}")

            # ... rest of your code ...
            markers_data.append({
                "name": str(location_name).strip(),
                "lat": float(lat),
                "lng": float(lng),
                # ... other data ...
            })
        print(f"Total markers processed: {len(markers_data)}")
        return markers_data

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE_PATH}. Please check path and filename.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred in get_marker_data: {e}")
        return []
