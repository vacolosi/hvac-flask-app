from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from collections import Counter
import os

app = Flask(__name__)

CSV_FILE = 'duct_data.csv'

# Create the CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Room", "CFM", "Duct_Size_Inches", "Location"]).to_csv(CSV_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form input
        room = request.form['room']
        cfm = int(request.form['cfm'])
        duct_size = request.form['duct_size']
        location = request.form['location']

        # Append to CSV file
        new_entry = pd.DataFrame([{
            "Room": room,
            "CFM": cfm,
            "Duct_Size_Inches": duct_size,
            "Location": location
        }])
        new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)

        # Redirect to clear the form
        return redirect('/')

    # Load full dataset from CSV
    df = pd.read_csv(CSV_FILE)

    # Summaries
    summary = df.groupby("Location")["CFM"].sum().reset_index()
    duct_counts = Counter(df["Duct_Size_Inches"])

    return render_template('index.html',
                           table=df.to_dict(orient='records'),
                           summary=summary,
                           duct_counts=duct_counts)

@app.route('/download')
def download_csv():
    return send_file(CSV_FILE,
                     mimetype='text/csv',
                     download_name='duct_data.csv',
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)