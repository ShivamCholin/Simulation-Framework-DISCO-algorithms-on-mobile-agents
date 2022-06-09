from intersecting_lines import doIntersect
import numpy as np
import matplotlib.pyplot as plt
import math
def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))
def distance(x1,y1,x2,y2):
    return ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)

def dot(vx,vy,wx,wy): return vx*wx + vy*wy
def wedge(vx,vy,wx,wy): return vx*wy - vy*wx

def is_between(ax,ay,bx,by,cx,cy):
   vx = ax - bx
   vy = ay - by
   wx = bx - cx
   wy = by - cy
   return -0.001<wedge(vx,vy,wx,wy)< 0.001 and dot(vx,vy,wx,wy) > -0.001
def check_if_directly_visible(lines1,poly, j1,px,py):
    for j in lines1:
        if poly[j1] not in j and doIntersect(j[0][0],j[0][1],j[1][0],j[1][1],px,py,poly[j1][0],poly[j1][1]):
            return False
    if ([px,py] in poly):
        k= poly.index([px,py])
        if angle_between((lines1[k][1][0]-lines1[k][0][0],lines1[k][1][1]-lines1[k][0][1]),(lines1[k-1][0][0]-lines1[k-1][1][0],lines1[k-1][0][1]-lines1[k-1][1][1])) < angle_between((lines1[k][1][0]-lines1[k][0][0],lines1[k][1][1]-lines1[k][0][1]),(poly[j1][0]-lines1[k-1][1][0],poly[j1][1]-lines1[k-1][1][1])):
            return False
    else:
        for i in range(len(poly)):
            if i!=j1 and distance(px,py,poly[i][0],poly[i][1])<distance(px,py,poly[j1][0],poly[j1][1]) and is_between(px,py,poly[i][0],poly[i][1],poly[j1][0],poly[j1][1]):
                ang1=angle_between((px-poly[i][0],py-poly[i][1]),(poly[i-1][0]-poly[i][0],poly[i-1][1]-poly[i][1]))
                ang2=angle_between((px-poly[i][0],py-poly[i][1]),(poly[i+1][0]-poly[i][0],poly[i+1][1]-poly[i][1]))
                minang=min(ang1,ang2)
                maxang=max(ang1,ang2)
                if minang<180:
                    if maxang>180:
                        #print("vertex block", minang,maxang,poly[j1])
                        return False
    return True

def check_if_edge_gap(lines1,poly, j,px,py):
    k1=(px-poly[j][0],py-poly[j][1])
    k3=(poly[j-1][0]-poly[j][0],poly[j-1][1]-poly[j][1])
    k4=(poly[(j+1)%(len(poly))][0]-poly[j][0],poly[(j+1)%(len(poly))][1]-poly[j][1])
    angle1=angle_between(k1,k3)
    angle2=angle_between(k1,k4)
    min_angle=min(angle1,angle2)
    max_angle=max(angle1,angle2)
    if angle1>180 and angle2==0:
        return True
    if angle1<=180 and angle2==0:
        return False
    if angle1==0 and angle2<180:
        return True
    if angle1==0 and angle2>=180:
        return False
    if min_angle>180:
        return True
    if max_angle<180:
        return True
    return False


def check_line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False
    return True


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def find_reflection(lines1,gap_point,px,py,poly):
    #print("finding reflection")
    #print(gap_point)
    light_turner=0
    potential=[]
    linecount=[]
    for  k in range(len(poly)):
        if poly[k]!=gap_point and is_between(px,py,gap_point[0],gap_point[1],poly[k][0],poly[k][1]):
            potential.append(poly[k])
            linecount.append((k-1+len(poly))%len(poly))
    for l in  range(len(lines1)):
        if check_line_intersection(lines1[l],[[px,py],gap_point]):
            p1x,p1y=line_intersection(lines1[l],[[px,py],gap_point])
            #print("int",lines,p1x,p1y)
            if min(lines1[l][0][0],lines1[l][1][0])-0.001<=p1x<=max(lines1[l][0][0],lines1[l][1][0])+0.001 and min(lines1[l][0][1],lines1[l][1][1])-0.001<=p1y<=max(lines1[l][0][1],lines1[l][1][1])+0.001:
                potential.append([p1x,p1y])
                linecount.append(l)
                #print("found point")
    #print("potential", potential)
    potential1=[]
    linecount1=[]
    for j in range(len(potential)):
        if not 178<=angle_between((gap_point[0]-px,gap_point[1]-py),(potential[j][0]-px,potential[j][1]-py))<=182:
            if not (math.isclose(float(potential[j][0]),float(gap_point[0])) and math.isclose(float(potential[j][1]),float(gap_point[1]))):
                if not (math.isclose(float(potential[j][0]),float(px)) and math.isclose(float(potential[j][1]),float(py))):
                    if distance(px,py,potential[j][0],potential[j][1]) - distance(px,py,gap_point[0],gap_point[1])>0:
                        potential1.append(potential[j])
                        linecount1.append(linecount[j])
        #             else:
        #                 print("4",j)
        #         else:
        #             print("3",j)
        #     else:
        #         print("2",j)
        # else:
        #     print("1",j)
        #     print("angle",angle_between((gap_point[0]-px,gap_point[1]-py),(potential[j][0]-px,potential[j][1]-py)))
    k=potential1[0]
    k1=linecount1[0]
    #print("potential1",potential1)
    for j in range(len(potential1)):
        if distance(px,py,k[0],k[1])>distance(px,py,potential1[j][0],potential1[j][1]):
            k=potential1[j]
            k1=linecount1[j]
    #print("reflect", gap_point,k,potential1)
    return k,k1




def visibility_poly(poly,px,py):
    lines1=[]
    gap_points=[]
    vis_pol_points=[]
    for i in range(len(poly)):
        lines1+=[[poly[i-1],poly[i]]];
    start=0
    for j in range(len(poly)):
        if not check_if_edge_gap(lines1,poly,j,px,py) and check_if_directly_visible(lines1,poly,j,px,py):
            start=j
            lights_on=poly[j]
            break
    lights=True
    lights_set=False
    for j in range(start,len(poly)):
        #print("point", poly[j], " index ", j )
        if lights_set:
            if j==lights_on:
                #print("lights turned on")
                lights=True
                lights_set=False
        if check_if_directly_visible(lines1,poly,j,px,py):
            if poly[j][0]==px and poly[j][1]==py:
                vis_pol_points.append(poly[j])
                lights=True
            elif check_if_edge_gap(lines1,poly,j,px,py):
                #print("potential edge  gap found")
                if lights:
                    vis_pol_points.append(poly[j])
                    ref,lights_on=find_reflection(lines1,poly[j],px,py,poly)
                    vis_pol_points.append(ref)
                    #print("vert beofre ref", poly[j],ref)
                    #print("light turner set", lights_on)
                    lights=False
                    lights_set=True
                else:
                    ref,_=find_reflection(lines1,poly[j],px,py,poly)
                    vis_pol_points.append(ref)
                    vis_pol_points.append(poly[j])
                    #print("ref before ver", ref,poly[j])
                    lights=True
                    lights_set=False
            else:
                vis_pol_points.append(poly[j])
                #print("directly visible",poly[j])
                lights=True
        else:
            lights=False
    for j in range(0,start):
        #print("point", poly[j], " index ", j )
        if lights_set:
            if j==lights_on:
                #print("lights turned on")
                lights=True
                lights_set=False
        if check_if_directly_visible(lines1,poly,j,px,py):
            if poly[j][0]==px and poly[j][1]==py:
                vis_pol_points.append(poly[j])
                lights=True
            elif check_if_edge_gap(lines1,poly,j,px,py):
                #print("potential edge  gap found")
                if lights:
                    vis_pol_points.append(poly[j])
                    ref,lights_on=find_reflection(lines1,poly[j],px,py,poly)
                    vis_pol_points.append(ref)
                    #print("vert beofre ref", poly[j],ref)
                    #print("light turner set", lights_on)
                    lights=False
                    lights_set=True
                else:
                    ref,_=find_reflection(lines1,poly[j],px,py,poly)
                    vis_pol_points.append(ref)
                    vis_pol_points.append(poly[j])
                    #print("ref before ver", ref,poly[j])
                    lights=True
                    lights_set=False
            else:
                vis_pol_points.append(poly[j])
                #print("directly visible",poly[j])
                lights=True
        else:
            lights=False
    return vis_pol_points

    
    




if __name__ == "__main__":
    poly=[[0,4],[0,7],[2,9],[4,8],[2,6],[2,1],[6,2],[4,5],[6,9],[8,6],[9,2],[9,-3],[6,-1],[4,-3],[6,-6],[9,-6],[6,-9],[2,-9],[4,-8],[3,-5],[2,-7],[-1,-9],[-9,-9],[-9,9],[-7,6],[-7,-3],[-3,-7],[-3,-3],[-6,-1],[-3,4]]
    poly=[[-6, 1], [-6, -2], [-3, -2], [-3, 2], [-9, 2], [-9, 9], [-7, 9], [-7, 4], [-5, 4], [-5, 5], [-6, 5], [-6, 9], [-5, 9], [-5, 7], [-4, 7], [-4, 9], [0, 9], [0, 5], [-2, 5], [-2, 1], [1, 1], [1, 10], [6, 10], [6, 8], [3, 8], [3, 2], [6, 2], [6, 4], [5, 4], [5, 7], [8, 7], [8, 9], [10, 9], [10, 3], [8, 3], [8, 0], [9, 0], [9, -3], [6, -3], [6, -1], [0, -1], [0, -2], [5, -2], [5, -4], [9, -4], [9, -6], [5, -6], [5, -7], [7, -7], [7, -9], [3, -9], [3, -4], [2, -4], [2, -9], [-1, -9], [-1, -4], [-6, -4], [-6, -7], [-4, -7], [-4, -5], [-2, -5], [-2, -9], [-9, -9], [-9, -4], [-8, -4], [-8, -1], [-9, -1], [-9, 1]]
    px=2.5
    py=1
    lines1=[]
    gap_points=[]
    vis_pol_points=[]
    for i in range(len(poly)):
        lines1+=[[poly[i-1],poly[i]]];
    red=visibility_poly(poly,px,py)
    print(red)
    x1=[i[0] for i in poly]+[poly[0][0]]
    y1=[i[1] for i in poly]+[poly[0][1]]
    # x2=[i[0] for i in red]
    # y3=[i[1] for i in red]
    # x,y=np.array(red).T
    # plt.scatter(x,y)
    plt.plot(px,py,'o')
    x2=[i[0] for i in red]+[red[0][0]]
    y3=[i[1] for i in red]+[red[0][1]]
    plt.plot(x2, y3, linewidth = 3,
            marker='o', color='red')
    plt.plot(x1, y1, label = "line 1", color='blue')
    plt.show()

