# Group 16 : Traffic Analysis Dashboard

<img src="Dashboard/Authority Analysis.png" alt="Image of Prototype Data Visualization Dashboard" width="200">

## File Roles

* Raw Data: `traffic.csv`
* Spark-Processed Data: `part-00000-cb8e687c-aeb8-4716-8c68-5061bd34f1b3-c000.snappy.parquet` 
* Spark Script: `trafficjob.py`
* Data Dashboard Source Code: `demo.py`


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

1. Clone the repo using,
```
git clone https://github.com/unlucky-shen/WQD7008-GA2.git
```
2. Navigate into the repo,
```
cd WQD7008-GA2/
```
3. Setup a Python Virtual environment with packages stated above.
4. Make sure `.parquet` data file is in the same directory as the virtual environment.
5. Activate the python environment
6. To run the dashboard locally on your device, run 
```
streamlit run demo.py
``` 

Alternatively, you can use, 
```
uv run streamlit run demo.py
``` 
straight away in the terminal if you are using uv-astral.

7. Dashboard will pop up in your default browser.
