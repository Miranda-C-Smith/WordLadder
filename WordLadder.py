#Miranda Smith
#00963796

from collections import deque
import sys

#To Run
#give dictionary and start and end word
#start and end word must be same length
def main():

    #Get start and end word
    start = "fool"
    end = "pope"
    start.lower()
    end.lower()

    #search type; Options: BFS = 1, DFS = 2, Informed = 3
    searchType = 1
    
    if len(start) != len(end):
        print("Start and End words not the same length. Please enter new words.")
        exit
        
    #Import Dictionary, only words of same length
    with open("words4letter.txt") as dictFile:
        dictionary = [ word.strip().lower() for word in dictFile if len(word.strip()) == len(start)]

    #find word ladder
    SearchSpaceTree = WordLadder(start, end, dictionary, searchType)
    PrintWordLadder(SearchSpaceTree, end)

def WordLadder(start, end, dictionary, searchType):
    #add start search space tree
    SearchTree = {}
    SearchTree[start]={"parent": '', "children": FindChildren(start,dictionary), "explored": True }
    #Add those children to the tree
    for node in SearchTree[start]["children"]:
        SearchTree[node] = {"parent": start, "explored": False}
        
    #if start = end; DONE; PRINT
    if(start == end):
        return SearchTree
    
    currentWord = start
    #lastWord = start
    while(currentWord != end):
        #decide next word
        if searchType == 1:
            currentWord = BFS(SearchTree, currentWord)
        elif searchType == 2:
            currentWord = DFS(SearchTree, currentWord)
        else:
            currentWord = InformedSearch(SearchTree, currentWord)

        #If no options left it was a failure
        if currentWord == '':
            print("No word ladder found between " + start + " and " + end)
            sys.exit()
            
        #explore the next chosen word
        SearchTree[currentWord]["children"]= FindChildren(currentWord,dictionary)
        SearchTree[currentWord]["explored"]= True

        #Add those children to the tree
        for node in SearchTree[currentWord]["children"]:
            #Dont add it if there is already an entry
            if node not in SearchTree:
                SearchTree[node] = {"parent": currentWord, "explored": False}
        #lastWord = currentWord
        
    return SearchTree


def FindChildren(word, dictionary):
    children = []
    for prospectiveChild in dictionary:
        #if difference bewteen word and child == 1 add to children list
        differences = 0
        for x in range(len(word)):
            if word[x] != prospectiveChild[x]:
                differences += 1
                if differences > 1:
                    break
        if differences == 1:
            children.append(prospectiveChild)

    return children


def BFS(SearchTree, currentWord, fringe=deque([])):
    #Find the next node to explore, no repeats
    #Use Queue
    nextWord = ''
    fringe.extend(SearchTree[currentWord]["children"])

    try:
        nextWord = fringe.popleft()
        while SearchTree[nextWord]["explored"]== True:
            nextWord = fringe.popleft()
    except IndexError:
        nextWord = ''
    return nextWord

def DFS(SearchTree, currentWord, fringe=deque([])):
    #Find the next node to explore, no repeats
    #Use Stack
    nextWord = ''
    fringe.extend(SearchTree[currentWord]["children"])

    try:
        nextWord = fringe.pop()
        while SearchTree[nextWord]["explored"]== True:
            nextWord = fringe.pop()
    except IndexError:
        nextWord = ''
       
    return nextWord

def InformedSearch():
    return

def PrintWordLadder(SearchTree, end):
    #backtrack and find the solution that was found from the graph
    path = []

    x = end
    while SearchTree[x]["parent"] != '' :
        path.insert(0, x)
        x = SearchTree[x]["parent"]
    path.insert(0,x)
    
    print(path[0], end="")
    for x in path[1:] :
        print(" -> " + x, end="")
    
    #print(SearchTree)

if __name__ == "__main__":
    main()
