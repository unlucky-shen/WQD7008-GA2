# GROUP 16 : TRAFFIC ANALYSIS DASHBOARD

## Tools
#### 1. Amazon Web Service

* Storage & Data Lake: S3
* EMR on EC2 Cluster
* Data Processing: Apache Spark
* Cloud Infrastructure: Elastic MapReduce (EMR)
* Resource Management: Apache Hadoop Yarn
* Data Format: Apache Parquet (Snappy Compressed)

#### 2. Application Layer (Data Visualization Dashboard)

Python was used for the application layer using **streamlit** library.

    * Packages used,
    ```
    pip install streamlit numpy pandas pyarrow statsmodels plotly
    ```

    * Or using uv-astral,
    ```
    uv add streamlit numpy pandas pyarrow statsmodels plotly
    ```

## Steps to Reproduce

1. Setup a Python Virtual environment with packages stated above.
2. Make sure `.parquet` data is in the same directory as the virtual environment.
3. Activate the python environment
4. To run the dashboard locally on your device, run `streamlit run demo.py`. Alternatively, you can use `uv run streamlit run demo.py` straight away in the terminal if you are using uv-astral.
5. Dashboard will pop up in your default browser.
