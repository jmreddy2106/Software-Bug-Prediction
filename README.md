# Software-Bug-Prediction

Before delivering any software application to clients, it must be tested that it meets it’s the functional and non-functional requirements. Software testing is often paired with software
reliability prediction models, so that the overall testing time required for the system to reach a specific failure intensity level can be estimated. It has been reported that the cost of fixing a bug
in later stages of the software development cycle can be very expensive when compared to the development phase. Therefore, one must take this into account and try to find and fix bugs as
early as possible. Software repositories contain historical and valuable information about the overall development of software systems. Mining software repositories (MSR) is nowadays
considered one of the most interesting growing fields within software engineering. MSR focuses on extracting and analyzing data available in software repositories to uncover interesting, useful,
and actionable information about the system. In this project, we extract the Quality Metrics from the repositories using python libraries like pydriller. These metrics can be used to predict the
high-risk areas. So, that testers can prioritize these risky areas to unveil the bugs which can reduce the time required for testers and improve the productivity of the system. 


## Python Packages
pydriller
pandas
sklearn
seaborn
matplotlib
flask


## Metrics used in this project
-> Code Churn
-> Commits Count 
-> Hunks Count
-> Lines Count
