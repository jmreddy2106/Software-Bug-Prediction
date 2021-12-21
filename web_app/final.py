import pandas as pd
# from datetime import datetime
# import numpy as np
from pydriller import RepositoryMining

from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount


def extract_data(link, name):

    st = ""
    i = 1
    mod_dict = {}
    j = 1
    stidx = 0
    cfl = set()
    modifiedAddRemoved = set()
    modifiedFilesList = set()
    bugKeys = ['fix', 'correct', 'bug', 'error', 'remove', 'rework']
    for commit in RepositoryMining(link).traverse_commits():
        st = "Commit " + str(i)
        # print(len(commit.modifications))
        for m in commit.modifications:
            if stidx == 0:
                start_date = commit.committer_date
                stidx = 1
            for z in bugKeys:
                if z in str(commit.msg).lower():
                    cfl.add(m.new_path)
                    break
            else:
                if m.change_type.name == "MODIFY":
                    modifiedFilesList.add(m.new_path)
                    if m.added > 0 and m.removed > 0:
                        modifiedAddRemoved.add(m.new_path)
            if m.filename not in mod_dict:
                mod_dict[m.new_path] = {"Commit": st, "Modified": m.new_path, "Commit msg": commit.msg,
                                        "Complexity": m.complexity, "Nol Added": m.added,
                                        "Nol Removed": m.removed, "No of lines in file": m.nloc,
                                        "Token Count": m.token_count,
                                        "No of Changed Methods": len(m.changed_methods),
                                        "No of Methods": len(m.methods)}
            else:
                mod_dict[m.new_path] = {"Modified": m.new_path,
                                        "Commit msg": mod_dict[m.filename]["Commit msg"] + "##" + commit.msg,
                                        "Complexity": m.complexity,
                                        "Nol Added": mod_dict[m.filename]["Nol Added"] + m.added,
                                        "Nol Removed": mod_dict[m.filename]["Nol Removed"] + m.removed,
                                        "No of lines in file": m.nloc, "Token Count": m.token_count,
                                        "No of Changed Methods": mod_dict[m.filename]["No of Changed Methods"] + len(
                                            m.changed_methods),
                                        "No of Methods": len(m.methods)}
            j += 1
            # print(mod_dict)
        end_date = commit.committer_date
        i += 1
    mdf = pd.DataFrame(mod_dict)
    tmdf = mdf.T
    tmdf.dropna()
    tmdf = tmdf[tmdf.Complexity.notnull()]
    tmdf.to_csv(name + 'Modifications.csv')
    print("completed")
    # print(modifiedFilesList)

    metric = CodeChurn(path_to_repo=link, since=start_date, to=end_date)
    files_count = metric.count()
    files_max = metric.max()
    files_avg = metric.avg()
    print("code churn completed")
    print(len(files_count))

    metric = CommitsCount(path_to_repo=link, since=start_date, to=end_date)
    files = metric.count()
    print("Commits Count Completed")
    print(len(files))

    metric = HunksCount(path_to_repo=link, since=start_date, to=end_date)
    Hunksfiles = metric.count()
    print("Hunks count completed")
    print(len(Hunksfiles))

    metric = LinesCount(path_to_repo=link, since=start_date, to=end_date)
    added_count = metric.count_added()
    added_max = metric.max_added()
    added_avg = metric.avg_added()
    removed_count = metric.count_removed()
    removed_max = metric.max_removed()
    removed_avg = metric.avg_removed()
    print('Lines Count Completed')
    print(len(added_count))
    pml = {"Code Churn": [files_count, files_max, files_avg], "Commits Count": [files], "Hunks Count": [Hunksfiles],
           "Lines Count": [added_count, added_max, added_avg, removed_count, removed_max, removed_avg]}
    pm = {}

    for i in files_count:
        pm[i] = {"Code Churn Files Count": files_count[i], "Code Churn Files Max": files_max[i],
                 "Code Churn Files Avg": files_avg[i],
                 "Commits Count": files[i], "Hunks Count": Hunksfiles[i], "Added Lines Count": added_count[i],
                 "Added Lines Max": added_max[i],
                 "Added Lines avg": added_avg[i], "Removed Lines Count": removed_count[i],
                 "Removed Lines max": removed_max[i],
                 "Removed Lines avg": removed_avg[i]
                 }

    pmdf = pd.DataFrame(pm)
    tpmdf = pmdf.T
    tpmdf.dropna()

    tpmdf.to_csv(name + 'ProcessMetrics.csv')
    print("Completed")

    fd = {}
    for i in files_count:
        fd[i] = {"File Name": i, "Commit msg": mod_dict[i]["Commit msg"], "Complexity": mod_dict[i]["Complexity"],
                 "Nol Added": mod_dict[i]["Nol Added"], "Nol Removed": mod_dict[i]["Nol Removed"],
                 "No of lines in file": mod_dict[i]["No of lines in file"], "Token Count": mod_dict[i]["Token Count"],
                 "No of Changed Methods": mod_dict[i]["No of Changed Methods"],
                 "No of Methods": mod_dict[i]["No of Methods"],
                 "Code Churn Files Count": pm[i]["Code Churn Files Count"],
                 "Code Churn Files Max": pm[i]["Code Churn Files Max"],
                 "Code Churn Files Avg": pm[i]["Code Churn Files Avg"], "Commits Count": pm[i]["Commits Count"],
                 "Hunks Count": pm[i]["Hunks Count"], "Added Lines Count": pm[i]["Added Lines Count"],
                 "Added Lines Max": pm[i]["Added Lines Max"], "Added Lines avg": pm[i]["Added Lines avg"],
                 "Removed Lines Count": pm[i]["Removed Lines Count"], "Removed Lines max": pm[i]["Removed Lines max"],
                 "Removed Lines avg": pm[i]["Removed Lines avg"]
                 }
        if i in cfl:
            fd[i]["BugLabelLevel"] = 2
            fd[i]["CommitBug"] = 1
            fd[i]["AddRemoved"] = 0
        elif i in modifiedFilesList:
            fd[i]["BugLabelLevel"] = 1
            fd[i]["CommitBug"] = 0
            if i in modifiedAddRemoved:
                fd[i]["AddRemoved"] = 1
            else:
                fd[i]["AddRemoved"] = 0
        else:
            fd[i]["BugLabelLevel"] = 0
            fd[i]["CommitBug"] = 0
            fd[i]["AddRemoved"] = 0
        if (i in cfl) or (i in modifiedAddRemoved):
            fd[i]["CommitAddRemoved"] = 1
        else:
            fd[i]["CommitAddRemoved"] = 0

    fidf = pd.DataFrame(fd)
    tfidf = fidf.T

    tfidf.dropna()
    tfidf = tfidf[tfidf.Complexity.notnull()]
    tfidf.to_csv(name + 'FinalSet.csv')
    file_name = name
    tfidf.to_csv(file_name+".csv")
    print("Final Completed")


# extract_data("https://github.com/jmreddy2106/amzon-reviews.git", "Example")
