\# CS14 Deployment Preparation



This branch prepares the prototype for cloud deployment.



\## Main modules



\- bridge/: main entry for researcher and participant web pages

\- researcher login/: researcher login frontend

\- researcher main/: researcher news post creation frontend and scraping API

\- CS14\_Temp117-Backend/: computer vision and eye-tracking backend

\- project\_database/: PostgreSQL database layer



\## Local run



```bash

pip install -r requirements.txt

python run\_prototype.py --host 0.0.0.0

