def onSegment(px,py, qx, qy, rx,ry):
    if ( (qx <= max(px, rx)) and (qx >= min(px, rx)) and
           (qy <= max(py, ry)) and (qy >= min(py, ry))):
        return True
    return False
 
def orientation(px,py, qx,qy, rx,ry):
     
    val = (float(qy - py) * (rx - qx)) - (float(qx - px) * (ry - qy))
    if (val > 0):
         
        # Clockwise orientation
        return 1
    elif (val < 0):
         
        # Counterclockwise orientation
        return 2
    else:
         
        # Collinear orientation
        return 0
 
# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1x,p1y,q1x,q1y,p2x,p2y,q2x,q2y):
     
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1x,p1y, q1x,q1y, p2x,p2y)
    o2 = orientation(p1x,p1y, q1x,q1y, q2x,q2y)
    o3 = orientation(p2x,p2y, q2x,q2y, p1x,p1y)
    o4 = orientation(p2x,p2y, q2x,q2y, q1x,q1y)
 
    # General case
    if o1==0 or o2==0 or o3==0 or o4==0:
        return False
    if ((o1 != o2) and (o3 != o4)):
        return True
 
    # If none of the cases
    return False