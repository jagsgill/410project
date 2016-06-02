from web import visualizer
import sys
import os
import shutil
import json
from git import *
from subprocess import *
from tools import fuser


def main(argv):
    global target
    opt = argv[0]
    target = extract_name(argv[1])
    if opt == "getRepo":
        try:
            git_pull(argv[1])
        except Exception, e:
            print (str(e))
    elif opt == "GenerateJSON":
        generateJson()
        print "do GenerateJSON"
    elif opt == "GenerateGraph":
        visualizer.begin()
    elif opt == "extractname":
        extract_name(argv[1])
    else:
        usage()

def extract_name(url):
    name = url[:-4]
    lastSlashIndex = 0
    for i,char in enumerate(url):
        if char == '/':
            lastSlashIndex = i      
    name = name[lastSlashIndex+1:]                            
#    print("Name: %s\n" % name)
    return name

def git_pull(git_dir):
    if not os.path.isdir("./" + target):
        os.makedirs(target)
        Repo.clone_from(git_dir, "./" + target)
    else:
        print "/Target folder exist, please remove it to get new repository"

def generateJson():
    if not os.path.isdir("./web/" + target + "/static/gravatars"):
        os.makedirs("./web/" + target + "/static/gravatars")
    if os.name is 'nt':
        log_location = os.path.dirname(os.path.realpath(__file__)) +"\PMDResult\\" + target
    else:
        log_location = os.path.dirname(os.path.realpath(__file__)) +"/PMDResult/" + target
    # generate and parse gitlog
    generate_git_log()
    print("*** Log location: %s \n" % log_location)
    commits = fuser.parse_gitlog(log_location, target)
    # filter out commits without any changes
    commit_with_changes = []
    hashes = []
    for commit in commits:
        if len(commit.fileChanges) > 0:
            commit_with_changes.append(commit)
            hashes.append(commit.hash)
    # PMD these commits and parse them
    print("$$$$$$$  $$$$$$$$  $$$$$$$ " + str(hashes))
    PMD(hashes)
    pmd = fuser.parse_PMD(log_location)
    #fuse them to JSON
    result = fuser.fuse_to_JSON(commit_with_changes, pmd, target)
    count = 0
    for r in result:
        with open('web/' + target + '/static/'+str(count)+'.json' , "w") as output:
            output.write(json.dumps(r))
        count = count + 1



def generate_git_log():
    g = Git('./' + target + '/')
    gitLog = g.log("--reverse","--numstat")
    if not os.path.isdir("./PMDResult/" + target):
        os.makedirs("PMDResult/" + target)
    with open('./PMDResult/' + target + '/gitLog.txt','w') as r:
        r.write(gitLog)
    print ("gitLog.txt is placed in PMDResult")

def PMD(commits):
    g = Git('./' + target)

    # create a branch for all commits
    # will reduce branch one we figure out the what to left out
    for c in commits:
        g.branch(c, c)
    print (g.branch())

    # run PMD to ./Target
    # place results in PMDResult
    i = 1
    for b in commits:
        g.checkout(b)
        if os.name is 'nt':
            os.system("tools\\pmd-bin-5.4.2\\bin\\run.sh pmd -d ./" + target  + " -format xml "
                  "-R java-basic,java-coupling,java-design,java-codesize > " +
                  "PMDResult\\" + target + "\\commit" + str(i) + ".xml")

        else:
            os.system("tools/pmd-bin-5.4.2/bin/run.sh pmd -d ./" + target + " -format xml "
                  "-R java-basic,java-design,java-codesize > " +
                  "PMDResult/" + target + "/commit" + str(i) + ".xml")
        i = i + 1
        # java-basic,java-coupling,java-design,java-codesize 

def usage():
    print "Usage: main.py <option> "
    print "option: getRepo <git repo address> - perform 'git pull' with given repoURL at ./target"
    print "        GenerateJSON <git repo address> - generate JSON from the fuser "
    print "        GenerateGraph <git repo address> - generate the result with D3 using JSON"


target = ""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    else:
        main(sys.argv[1:])
