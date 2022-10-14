from pyamaze import maze,agent,COLOR,textLabel
import time

def shortestPath(m):
    start=(m.rows,m.cols)
    
    visited={} # already visited cells
    revPath={} # derive shortest path
    unvisited={cell:float('inf') for cell in m.grid}
    unvisited[start]=0

    while unvisited:
        currCell=min(unvisited,key=unvisited.get)
        visited[currCell]=unvisited[currCell]
        if currCell==m._goal:
            break # work backwards to get shortest path
        for d in 'NEWS':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    child=(currCell[0],currCell[1]+1)
                elif d=='W':
                    child=(currCell[0],currCell[1]-1)
                elif d=='S':
                    child=(currCell[0]+1,currCell[1])
                elif d=='N':
                    child=(currCell[0]-1,currCell[1])
                if child in visited:
                    continue
                dist= unvisited[currCell]+1

                if dist < unvisited[child]:
                    unvisited[child]=dist
                    revPath[child]=currCell
        unvisited.pop(currCell)
    
    path={}
    cell=m._goal
    while cell!=start: # work backwards to get shortest path
        path[revPath[cell]]=cell
        cell=revPath[cell]
    
    return path,visited[m._goal]
            
if __name__=='__main__':
    m=maze()
    m.CreateMaze(loadMaze="maze10.csv")
    # m.CreateMaze(loadMaze="maze50.csv")
    # m.CreateMaze(loadMaze="maze100.csv")

    startTime = time.perf_counter()
    path,length=shortestPath(m)
    endTime = time.perf_counter()
    textLabel(m,'Path Length',length+1)
    textLabel(m,'Runtime',round(endTime - startTime, 4))

    print(f"Runtime {endTime - startTime:0.4f} seconds")
    a=agent(m,color=COLOR.cyan,filled=True, footprints=True)
    m.tracePath({a:path}, delay=0)

    m.run()