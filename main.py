import os
from google.cloud import storage, bigquery
import pandas as pd
import io

# Set the environment variable for Application Default Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sales-accelerator-425301-b074db1b7079.json"

# Initialize clients
storage_client = storage.Client()
bigquery_client = bigquery.Client()

def analyze_sales_report(request):
    # Parse the CSV file from the request
    file = request.files['file']
    content = file.read().decode('utf-8')
    sales_df = pd.read_csv(io.StringIO(content))
    
    sales_df['Total Sales'] = sales_df['Quantity'] * sales_df['Price']
    # Process and store data in BigQuery
    table_id = "sales-accelerator-425301.sales_ds.sales_table"
    job = bigquery_client.load_table_from_dataframe(sales_df, table_id)
    job.result()  # Wait for the job to complete

    # Generate summary
    summary = sales_df.groupby('Product')['Total Sales'].sum().reset_index()
    summary_html = summary.to_html()

    return summary_html
