from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
import time

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)
def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    searchPath=[start]
    while not open.empty():
        currCell=open.get()[2]
        searchPath.append(currCell)
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell,(1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath, searchPath

if __name__=='__main__':
    m=maze()
    m.CreateMaze(loadMaze="maze10.csv")
    # m.CreateMaze(loadMaze="maze50.csv")
    # m.CreateMaze(loadMaze="maze100.csv")

    startTime = time.perf_counter()
    path, search=aStar(m)
    endTime = time.perf_counter()

    a=agent(m,footprints=True)
    m.tracePath({a:path},delay=0)
    l=textLabel(m,'A Star Path Length',len(path)+1)
    l=textLabel(m,'Runtime',round(endTime - startTime, 4))

    m.run()