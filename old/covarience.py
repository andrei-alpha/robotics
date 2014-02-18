xs = [0.4, 3.4, 0.86, 3.4, 2.3, 4.9, 1.4, 2.9, 0.4, 1.3]
ys = [0.2, 4, 0.2, 3.6, 2.2, 1.9, 0.3, 3, 0.4, 1.9]

meanX = reduce (lambda x,y: x + y, xs) / 10.0
meanY = reduce (lambda x,y: x + y, ys) / 10.0

m00 = reduce (lambda x,y : x + y, map (lambda x: (x - meanX) * (x - meanX), xs) ) / 10
m01 = reduce (lambda x,y : x + y, map (lambda x,y: (x - meanX) * (y - meanY), xs, ys) ) / 10
m10 = reduce (lambda x,y : x + y, map (lambda x,y: (y - meanY) * (x - meanX), xs, ys) ) / 10
m11 = reduce (lambda x,y : x + y, map (lambda y: (y - meanY) * (y - meanY), xs) ) / 10

print '|', m00, m01, '|'
print '|', m10, m11, '|'
