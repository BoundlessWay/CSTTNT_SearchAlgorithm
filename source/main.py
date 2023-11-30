from re import S
import matplotlib.pyplot as plt
import math
import os
from pathlib import Path

class NODE:
    def __init__(self, x, y, parent = None, bonus_Point = 0):
        self.x = x
        self.y = y
        self.parent_Node = parent
        self.bonus_Point = bonus_Point
        self.adjacency_List = []
        
    
class CONTROLLER:
    
    def __init__(self):
        self.cur_Path = os.path.dirname(os.path.abspath(__file__))
        self.folder_Input_Path = ""
        self.folder_Output_Path = ""
        # Ma trận bản đồ ở dạng text
        self.matrix = []
        # Ma trận bản đồ bao gồm các Node tạo thành đồ thị
        self.graph = []
        self.bonus_Points = []
        self.start_Point = ()
        self.end_Point = ()
        self.route = []
        self.cost_Shortest_Path = '0'
        self.heuristic1 = {}
        self.heuristic2 = {}


    # Hàm đọc các Map level__1 và level__2
    def readMap(self, filename):
        with open(filename, 'r') as file:
            self.bonus_Points = []
            for i in range(int(next(file)[:-1])):
                x, y, point = map(int, next(file)[:-1].split(' '))
                self.bonus_Points.append([x, y, point])
            text = file.read()
            self.matrix = [list(i) for i in text.splitlines()]
        
        # Duyệt qua ma trận và tạo Node trong đồ thị từ ma trận
        self.graph = [[None for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if (self.matrix[i][j] != 'x'):
                    self.graph[i][j] = NODE(i, j)
                    for bonus_Point in self.bonus_Points:
                        if i == bonus_Point[0] and j == bonus_Point[1]:
                            self.graph[i][j].bonus_Point = bonus_Point[2]
                            break
                if (self.matrix[i][j] == 'S'):
                    self.start_Point = self.graph[i][j]
                elif (self.matrix[i][j] == ' '):
                    if (i == 0) or (i == len(self.matrix) - 1) or (j == 0) or (j == len(self.matrix[0]) - 1):
                        self.end_Point = self.graph[i][j]
                else: pass
                    

        # Duyệt qua đồ thị, thêm danh sách kề các Node trong đồ thị          
        for i in range(len(self.graph)):
            for j in range(len(self.graph[0])):
                if self.graph[i][j] is not None:
                    if  (i > 0) and self.graph[i - 1][j] is not None:
                        self.graph[i][j].adjacency_List.append([self.graph[i - 1][j], 1])
                    if  (i < len(self.graph) - 1) and self.graph[i + 1][j] is not None:
                        self.graph[i][j].adjacency_List.append([self.graph[i + 1][j], 1]) 
                    if (j > 0) and self.graph[i][j - 1] is not None:
                        self.graph[i][j].adjacency_List.append([self.graph[i][j - 1], 1])
                    if (j < len(self.graph[0]) - 1) and self.graph[i][j + 1] is not None:
                        self.graph[i][j].adjacency_List.append([self.graph[i][j + 1], 1])
                    h1 = math.sqrt((self.end_Point.x - i)**2 + (self.end_Point.y - j)**2)
                    h2 = math.fabs(self.end_Point.x - i) + math.fabs(self.end_Point.y - j)
                    self.heuristic1[self.graph[i][j]] = h1
                    self.heuristic2[self.graph[i][j]] = h2
                   
                   
    def readAdvanceMap(self, filename):
        pass
        
           
    def visualizeMaze(self):
        walls = [(i, j) for i in range(len(self.matrix)) for j in range(len(self.matrix[0])) if self.matrix[i][j]=='x'] 
        if self.route:
            direction=[]
            for i in range(2,len(self.route)):
                if self.route[i][0]-self.route[i-1][0]>0:
                    direction.append('v') 
                elif self.route[i][0]-self.route[i-1][0]<0:
                    direction.append('^')      
                elif self.route[i][1]-self.route[i-1][1]>0:
                    direction.append('>')
                else:
                    direction.append('<')

        
        ax=plt.figure(dpi=100).add_subplot(111)
        

        for i in ['top','bottom','right','left']:
            ax.spines[i].set_visible(False)

        plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                    marker='X',s=100,color='black')
        
        plt.scatter([i[1] for i in self.bonus_Points],[-i[0] for i in self.bonus_Points],
                    marker='P',s=100,color='green')

        plt.scatter(self.start_Point.y,-self.start_Point.x,marker='*',
                    s=100,color='gold')

        if self.route:
            for i in range(len(self.route)-2):
                plt.scatter(self.route[i+1][1],-self.route[i+1][0],
                            marker=direction[i],color='silver')

        plt.text(self.end_Point.y,-self.end_Point.x,'EXIT',color='red',
            horizontalalignment='center',
            verticalalignment='center')
        plt.xticks([])
        plt.yticks([])

        
    def writeMap(self, path_Folder, algo_Name):
        if 'heuristic' in algo_Name:
            path_Folder = os.path.join(path_Folder, algo_Name[:algo_Name.index('heuristic')-1])
        else: path_Folder = os.path.join(path_Folder, algo_Name)
        if not os.path.exists(path_Folder):
            os.makedirs(path_Folder)
        plt.savefig(os.path.join(path_Folder, algo_Name + '.jpg'))
        plt.close()
        with open(os.path.join(path_Folder, algo_Name + '.txt'), 'w') as file:
            if (self.route is None): file.write('NO')
            else: file.write(self.cost_Shortest_Path)

    
    def bfs(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        queue = []
        visited = []
        self.route = []
        queue.append(src)
        while True:
            if len(queue) == 0:
                self.route = None
                return
            vertex = queue.pop(0)
            visited.append(vertex)
           
            if (vertex.x == des.x and vertex.y == des.y):
                break
            for adj_Vertex in vertex.adjacency_List:
                if (adj_Vertex[0] not in queue) and (adj_Vertex[0] not in visited):
                    adj_Vertex[0].parent_Node = vertex
                    queue.append(adj_Vertex[0])
                
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.cost_Shortest_Path = str(len(self.route) - 1)
        self.visualizeMaze()   
            
            
    def dfs(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        stack = []
        visited = []
        self.route = []
        stack.append(src)
        while True:
            if len(stack) == 0:
                self.route = None
                break
            vertex = stack.pop(0)
            visited.append(vertex)
            if (vertex.x == des.x and vertex.y == des.y):
                break
            pos = 0
            for adj_Vertex in vertex.adjacency_List:
                if (adj_Vertex[0] not in stack) and (adj_Vertex[0] not in visited):
                    adj_Vertex[0].parent_Node = vertex
                    stack.insert(pos, adj_Vertex[0])
                    pos += 1
                  
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.cost_Shortest_Path = str(len(self.route) - 1)
        self.visualizeMaze() 
      
    
    def ucs(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        priority_Queue = []
        visited = []
        self.route = []
        priority_Queue.append([src, 0])
        while True:
            if len(priority_Queue) == 0:
                self.route = None
                return
            # Đỉnh và chi phí tính từ điểm xuất phát
            vertex, cost = priority_Queue.pop(0)
            visited.append(vertex)
            
            if (vertex.x == des.x and vertex.y == des.y):
                self.cost_Shortest_Path = str(cost)
                break   
            for adj_Vertex in vertex.adjacency_List:
                if adj_Vertex[0] not in visited:
                    # Chi phí tính từ điểm xuất phát của đỉnh kề
                    adj_Cost = cost + adj_Vertex[1]
                    if (len(priority_Queue) == 0): 
                        priority_Queue.append([adj_Vertex[0], adj_Cost])  
                        adj_Vertex[0].parent_Node = vertex
                        continue      
                    i = 0
                    while i < len(priority_Queue):
                        if (priority_Queue[i][0].x == adj_Vertex[0].x and priority_Queue[i][0].y == adj_Vertex[0].y):
                            if priority_Queue[i][1] <= adj_Cost:
                                adj_Cost = None
                                break
                            else: 
                                del priority_Queue[i]
                                i -= 1
                        i += 1
                    # Đã tồn tại đường đi khác đến điểm này ngắn hơn nên không cần xét lại điểm này
                    if adj_Cost is None: continue
                    for i in range(len(priority_Queue)):
                        if (priority_Queue[i][1] > adj_Cost):
                            adj_Vertex[0].parent_Node = vertex
                            priority_Queue.insert(i, [adj_Vertex[0], adj_Cost])
                            break
                        if i == len(priority_Queue) - 1: 
                            priority_Queue.append([adj_Vertex[0], adj_Cost])
                            adj_Vertex[0].parent_Node = vertex
                    
                          
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.visualizeMaze()   
    
    
    # Heuristic1: Hàm đánh giá khoảng cách Euclid so với điểm đích
    # Đây là hàm heuristic nhất quán
    def gbfs_Heuristic1(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        priority_Queue = []
        visited = []
        self.route = []
        priority_Queue.append([src, self.heuristic1[src]])
        while True:
            if len(priority_Queue) == 0:
                self.route = None
                return
            # Đỉnh và chi phí ước tính so với điểm đích
            vertex, cost = priority_Queue.pop(0)
            visited.append(vertex)
            
            if (vertex.x == des.x and vertex.y == des.y):
                break   
            for adj_Vertex in vertex.adjacency_List:
                if adj_Vertex[0] not in visited:
                    # Chi phí ước tính so với điểm đích của đỉnh kề
                    adj_Cost = self.heuristic1[adj_Vertex[0]]
                    if (len(priority_Queue) == 0): 
                        priority_Queue.append([adj_Vertex[0], adj_Cost])  
                        adj_Vertex[0].parent_Node = vertex
                        continue      
                    i = 0
                    while i < len(priority_Queue):
                        if (priority_Queue[i][0].x == adj_Vertex[0].x and priority_Queue[i][0].y == adj_Vertex[0].y):
                            if priority_Queue[i][1] <= adj_Cost:
                                adj_Cost = None
                                break
                            else: 
                                del priority_Queue[i]
                                i -= 1
                        i += 1
                    # Đã tồn tại đường đi khác đến điểm này có chi phí ước tính ngắn hơn nên không cần xét lại điểm này
                    if adj_Cost is None: continue
                    for i in range(len(priority_Queue)):
                        if (priority_Queue[i][1] > adj_Cost):
                            adj_Vertex[0].parent_Node = vertex
                            priority_Queue.insert(i, [adj_Vertex[0], adj_Cost])
                            break
                        if i == len(priority_Queue) - 1: 
                            priority_Queue.append([adj_Vertex[0], adj_Cost])
                            adj_Vertex[0].parent_Node = vertex
                    
                          
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.cost_Shortest_Path = str(len(self.route) - 1)
        self.visualizeMaze()   
        
  
    # Heuristic2: Hàm đánh giá khoảng cách Manhattan so với điểm đích
    # Đây là hàm heuristic nhất quán
    def gbfs_Heuristic2(self, src = None, des = None): 
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        priority_Queue = []
        visited = []
        self.route = []
        priority_Queue.append([src, self.heuristic2[src]])
        while True:
            if len(priority_Queue) == 0:
                self.route = None
                return
            # Đỉnh và chi phí ước tính so với điểm đích
            vertex, cost = priority_Queue.pop(0)
            visited.append(vertex)
            
            if (vertex.x == des.x and vertex.y == des.y):
                break   
            for adj_Vertex in vertex.adjacency_List:
                if adj_Vertex[0] not in visited:
                    # Chi phí ước tính so với đỉnh đích của đỉnh kề
                    adj_Cost = self.heuristic2[adj_Vertex[0]]
                    if (len(priority_Queue) == 0): 
                        priority_Queue.append([adj_Vertex[0], adj_Cost])  
                        adj_Vertex[0].parent_Node = vertex
                        continue      
                    i = 0
                    while i < len(priority_Queue):
                        if (priority_Queue[i][0].x == adj_Vertex[0].x and priority_Queue[i][0].y == adj_Vertex[0].y):
                            if priority_Queue[i][1] <= adj_Cost:
                                adj_Cost = None
                                break
                            else: 
                                del priority_Queue[i]
                                i -= 1
                        i += 1
                    # Đã tồn tại đường đi khác đến điểm này có chi phí ước tính ngắn hơn nên không cần xét lại điểm này
                    if adj_Cost is None: continue
                    for i in range(len(priority_Queue)):
                        if (priority_Queue[i][1] > adj_Cost):
                            adj_Vertex[0].parent_Node = vertex
                            priority_Queue.insert(i, [adj_Vertex[0], adj_Cost])
                            break
                        if i == len(priority_Queue) - 1: 
                            priority_Queue.append([adj_Vertex[0], adj_Cost])
                            adj_Vertex[0].parent_Node = vertex
                    
                          
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.cost_Shortest_Path = str(len(self.route) - 1)
        self.visualizeMaze()   
    
    
    # Heuristic1: Hàm đánh giá khoảng cách Euclid so với điểm đích
    # Đây là hàm heuristic nhất quán
    def astar_Heuristic1(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        priority_Queue = []
        visited = []
        self.route = []
        priority_Queue.append([src, 0])
        while True:
            if len(priority_Queue) == 0:
                self.route = None
                return
            # Đỉnh và khoảng cách đường đi tính từ điểm xuất phát
            vertex, cost = priority_Queue.pop(0)
            visited.append(vertex)
            
            if (vertex.x == des.x and vertex.y == des.y):
                self.cost_Shortest_Path = str(cost)
                break   
            for adj_Vertex in vertex.adjacency_List:
                if adj_Vertex[0] not in visited:
                    # Chi phí ước tính so với điểm đích của đỉnh kề
                    adj_Cost = cost + adj_Vertex[1] + self.heuristic1[adj_Vertex[0]]
                    if (len(priority_Queue) == 0): 
                        priority_Queue.append([adj_Vertex[0], cost + adj_Vertex[1]])  
                        adj_Vertex[0].parent_Node = vertex
                        continue      
                    i = 0
                    while i < len(priority_Queue):
                        if (priority_Queue[i][0].x == adj_Vertex[0].x and priority_Queue[i][0].y == adj_Vertex[0].y):
                            if priority_Queue[i][1] + self.heuristic1[priority_Queue[i][0]] <= adj_Cost:
                                adj_Cost = None
                                break
                            else: 
                                del priority_Queue[i]
                                i -= 1
                        i += 1
                    # Đã tồn tại đường đi khác đến điểm này có chi phí ước tính ngắn hơn nên không cần xét lại điểm này
                    if adj_Cost is None: continue
                    for i in range(len(priority_Queue)):
                        if (priority_Queue[i][1] + self.heuristic1[priority_Queue[i][0]] > adj_Cost):
                            adj_Vertex[0].parent_Node = vertex
                            priority_Queue.insert(i, [adj_Vertex[0], cost + adj_Vertex[1]])
                            break
                        if i == len(priority_Queue) - 1: 
                            priority_Queue.append([adj_Vertex[0], cost + adj_Vertex[1]])
                            adj_Vertex[0].parent_Node = vertex
                    
                          
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.visualizeMaze()
    
    
    # Heuristic2: Hàm đánh giá khoảng cách Manhattan so với điểm đích
    # Đây là hàm heuristic nhất quán
    def astar_Heuristic2(self, src = None, des = None):
        if src is None: src = self.start_Point
        if des is None: des = self.end_Point
        priority_Queue = []
        visited = []
        self.route = []
        priority_Queue.append([src, 0])
        while True:
            if len(priority_Queue) == 0:
                self.route = None
                return
            # Đỉnh và khoảng cách đường đi tính từ điểm xuất phát
            vertex, cost = priority_Queue.pop(0)
            visited.append(vertex)
            
            if (vertex.x == des.x and vertex.y == des.y):
                self.cost_Shortest_Path = str(cost)
                break   
            for adj_Vertex in vertex.adjacency_List:
                if adj_Vertex[0] not in visited:
                    # Chi phí ước tính so với điểm đích của đỉnh kề
                    adj_Cost = cost + adj_Vertex[1] + self.heuristic2[adj_Vertex[0]]
                    if (len(priority_Queue) == 0): 
                        priority_Queue.append([adj_Vertex[0], cost + adj_Vertex[1]])  
                        adj_Vertex[0].parent_Node = vertex
                        continue  
                    i = 0
                    while i < len(priority_Queue):
                        if (priority_Queue[i][0].x == adj_Vertex[0].x and priority_Queue[i][0].y == adj_Vertex[0].y):
                            if priority_Queue[i][1] + self.heuristic2[priority_Queue[i][0]] <= adj_Cost:
                                adj_Cost = None
                                break
                            else: 
                                del priority_Queue[i]
                                i -= 1
                        i += 1
                    # Đã tồn tại đường đi khác đến điểm này có chi phí ước tính ngắn hơn nên không cần xét lại điểm này
                    if adj_Cost is None: continue
                    for i in range(len(priority_Queue)):
                        if (priority_Queue[i][1] + self.heuristic2[priority_Queue[i][0]] > adj_Cost):
                            adj_Vertex[0].parent_Node = vertex
                            priority_Queue.insert(i, [adj_Vertex[0], cost + adj_Vertex[1]])
                            break
                        if i == len(priority_Queue) - 1: 
                            priority_Queue.append([adj_Vertex[0], cost + adj_Vertex[1]])
                            adj_Vertex[0].parent_Node = vertex
                    
                          
        vertex = des
        self.route.append([vertex.x, vertex.y])
        while vertex.parent_Node is not None:
            vertex = vertex.parent_Node
            self.route.append([vertex.x, vertex.y])
        self.route.reverse()
        self.visualizeMaze()
  
     
    # Thuật toán tự đề xuất: 
    def algo1(self, src = None, des = None):
        
        # temp_Route = []
        # heuristic = {}
        # if src is None: src = self.start_Point
        # if des is None: des = self.end_Point
        # for bonus_point in self.bonus_Points:
        #     # Khoảng cách manhattan từ điểm thưởng đến nguồn
        #     a = math.fabs(bonus_point[0] - src.x) + math.fabs(bonus_point[1] - src.y)
        #     # Khoảng cách manhattan từ điểm thưởng đến đích
        #     b = math.fabs(bonus_point[0] - des.x) + math.fabs(bonus_point[1] - des.y)
        #     heuristic[bonus_point[2] + a + b] = self.graph[bonus_point[0]][bonus_point[1]]
        # sorted_Key_Heuristic = sorted(heuristic.keys())
        # point = heuristic[sorted_Key_Heuristic.pop(0)]
        # a = max(self.start_Point.x, self.end_Point.x)
        # b = min(self.start_Point.x, self.end_Point.x)
        # c = max(self.start_Point.y, self.end_Point.y)
        # d = min(self.start_Point.y, self.end_Point.y)
        # if point.x > a or point.x < b or point.y > c or point.y < d:
        #     des = self.end_Point
        # while True: 
        #     self.gbfs_Heuristic2(src, point)
        #     self.route.reverse()
        #     temp_Route.extend(self.route)
        #     self.gbfs_Heuristic2(point, des)
        #     self.route.reverse()
        #     temp_Route.extend
        pass
            
        
        
            
    def run(self):
        self.folder_Input_Path = os.path.join(Path(self.cur_Path).parent, "input")
        self.folder_Output_Path = os.path.join(Path(self.cur_Path).parent, "output")
        if not os.path.exists(self.folder_Output_Path):
            os.makedirs(self.folder_Output_Path)
           
        list_Folder_Input = os.listdir(self.folder_Input_Path)
        for i in range(len(list_Folder_Input)):
            list_File_Input = os.listdir(os.path.join(self.folder_Input_Path, list_Folder_Input[i]))
            for j in range(len(list_File_Input)):
                path_File_Input = os.path.join(self.folder_Input_Path, list_Folder_Input[i], list_File_Input[j])
                path_Folder_Output = os.path.join(self.folder_Output_Path, list_Folder_Input[i], list_File_Input[j][:-4])
                if not os.path.exists(path_Folder_Output):
                    os.makedirs(path_Folder_Output)

                if (list_Folder_Input[i] == 'level_1'):
                    self.readMap(path_File_Input)
                    self.bfs()
                    self.writeMap(path_Folder_Output, 'bfs')
                    self.dfs()   
                    self.writeMap(path_Folder_Output, 'dfs')
                    self.ucs()
                    self.writeMap(path_Folder_Output, 'ucs')
                    self.gbfs_Heuristic1()
                    self.writeMap(path_Folder_Output, 'gbfs_heuristic_1')
                    self.gbfs_Heuristic2()
                    self.writeMap(path_Folder_Output, 'gbfs_heuristic_2')
                    self.astar_Heuristic1()
                    self.writeMap(path_Folder_Output, 'astar_heuristic_1')    
                    self.astar_Heuristic2()   
                    self.writeMap(path_Folder_Output, 'astar_heuristic_2')          
                elif list_Folder_Input[i] == 'level_2':
                    pass
                    # self.readMap(path_File_Input)
                    # self.algo1()
                    # self.writeMap(path_Folder_Output, 'algo1')           

                else: self.readAdvanceMap(path_File_Input)
    



if __name__ == '__main__':
    Controller = CONTROLLER()
    Controller.run()
 
    
    
    
   

   
   
   
    
            