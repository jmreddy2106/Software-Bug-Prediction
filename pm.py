link="https://github.com/EpistasisLab/tpot.git"
import pandas as pd
from datetime import datetime
start_date=datetime(2015,11,3, 16, 8, 40)
end_date=datetime(2021, 1, 6, 10, 17, 46)


from pydriller.metrics.process.code_churn import CodeChurn
metric = CodeChurn(path_to_repo=link, since = start_date, to = end_date)
files_count = metric.count()
files_max = metric.max()
files_avg = metric.avg()
print("code churn completed")
print(len(files_count))
from pydriller.metrics.process.commits_count import CommitsCount
metric = CommitsCount(path_to_repo = link, since = start_date, to = end_date)
files = metric.count()
print("Commits Count Completed")
print(len(files))
from pydriller.metrics.process.hunks_count import HunksCount
metric = HunksCount(path_to_repo = link, since = start_date, to = end_date)
Hunksfiles = metric.count()
print("Hunks count completed")
print(len(Hunksfiles))
from pydriller.metrics.process.lines_count import LinesCount
metric = LinesCount( path_to_repo = link, since = start_date, to = end_date)
added_count = metric.count_added()
added_max = metric.max_added()
added_avg = metric.avg_added()
removed_count = metric.count_removed()
removed_max = metric.max_removed()
removed_avg = metric.avg_removed()
print('Lines Count Completed')
print(len(added_count))
from pydriller.metrics.process.contributors_count import ContributorsCount
metric = ContributorsCount(path_to_repo = link , since = start_date , to = end_date)
Contributorscount = metric.count()
minor = metric.count_minor()
print("Contirbutors Count Completed")
print(len(minor))
from pydriller.metrics.process.contributors_experience import ContributorsExperience
metric = ContributorsExperience(path_to_repo = link, since = start_date, to = end_date)
Expfiles = metric.count()
print('Contributors Exp completeed')
print(len(Expfiles))
pml={"Code Churn": [files_count,files_max,files_avg], "Commits Count": [files], "Hunks Count": [Hunksfiles], "Lines Count": [added_count,added_max,added_avg,removed_count,removed_max,removed_avg], "Contributors Count": [Contributorscount, minor], "Contributor Experience": [Expfiles]}
pm={}

for i in files_count:
    pm[i]={"Code Churn Files Count": files_count[i], "Code Churn Files Max": files_max[i], 
           "Code Churn Files Avg": files_avg[i],
            "Commits Count": files[i], "Hunks Count": Hunksfiles[i], "Added Lines Count": added_count[i], 
           "Added Lines Max": added_max[i],
           "Added Lines avg": added_avg[i], "Removed Lines Count": removed_count[i], "Removed Lines max": removed_max[i], 
           "Removed Lines avg": removed_avg[i], "Contributors Count": Contributorscount.get(i), "Contributors Minor": minor.get(i),
          "Contributor Experience": Expfiles.get(i)}

pmdf=pd.DataFrame(pm)
tpmdf=pmdf.T
tpmdf.to_csv(r'ProcessMetrics.csv')
print("Completed")
