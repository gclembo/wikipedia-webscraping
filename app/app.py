import pandas as pd
import sqlite3, json
from pathlib import Path
from flask import Flask, render_template


def load_data():
    file_path = Path(__file__)
    project_folder = file_path.resolve().parent.parent
    data_folder = project_folder / "data"

    db_filename = "wiki_data.db"

    conn = sqlite3.connect(data_folder / db_filename)
    df = pd.read_sql_query("SELECT * FROM pages_raw", conn)
    conn.close()
    return df


wiki_data = load_data()

app = Flask(__name__)

def make_data_list(col_name):
    return json.dumps(wiki_data[col_name].tolist())

@app.route("/")
def run_dashboard():
    return render_template(
        "dashboard.html",
        word_count=make_data_list("word_count"),
        source_count=make_data_list("source_count"),
        image_count=make_data_list("image_count"),
        titles=make_data_list("title"),
        published=make_data_list("published"),
        modified=make_data_list("modified")
    )

if __name__ == "__main__":
    app.run(debug=True)
