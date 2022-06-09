def slowed_simu3(movement,split):
    movement2=[]
    for temp1 in movement:
        l=[]
        for i in range(len(temp1)-1):
            x1=(temp1[i][0]-temp1[i+1][0])/split
            y1=(temp1[i][1]-temp1[i+1][1])/split
            for j in range(split):
                l.append([temp1[i][0]-x1*j,temp1[i][1]-y1*j])
        l.append(temp1[-1])
        movement2.append(l)
    return movement2