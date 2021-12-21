import pandas as pd
from pydriller import RepositoryMining
link = "https://github.com/EpistasisLab/tpot.git"
st = ""
i=1
modification_dictionary = {}
j=1
modifiedFilesList=set()
bugKeys=['Fix','Error','Remove','Error','Rework']
for commit in RepositoryMining(link).traverse_commits():
	st = "Commit "+str(i)
	    #print(len(commit.modifications))
	for m in commit.modifications:
		if m.change_type.name == "MODIFY":
			modifiedFilesList.add(m.filename)
		elif any(idx.lower() in commit.msg.lower() for idx in bugKeys):
			modifiedFilesList.add(m.filename)
		modification_dictionary[j] = {"Commit": st,"Commit msg":commit.msg, "Author": commit.author.name, "Modified": m.filename, 
                                   "Change Type": m.change_type.name, "Complexity": m.complexity, 
                                   "Nol Added": m.added, "Nol Removed": m.removed, "No of lines in file": m.nloc,
                                      "Token Count": m.token_count,
                                   "No of Changed Methods": len(m.changed_methods), "No of Methods": len(m.methods)}
		j += 1
		#print(modification_dictionary)
	i+=1
mdf=pd.DataFrame(modification_dictionary)
tmdf=mdf.T
tmdf.to_csv(r'Modifications.csv')
tmdf.dropna()
for i in tmdf["Complexity"]:
	print(type(i))
print(type(tmdf["Complexity"]))

print("completed")

