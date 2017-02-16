import numpy


# Mapping from zernike name to number (1-15)
zernikeNumbers = {
    'piston': 1,
    'tip': 2,
    'tilt': 3,
    'focus': 4,
    'astig1': 5,
    'astig2': 6,
    'coma1': 7,
    'coma2': 8,
    'trefoil1': 9,
    'trefoil2': 10,
    'spherical': 11,
    'z12': 12,
    'z13': 13,
    'z14': 14,
    'z15': 15
}

zernikeDegFreqToNum = {
  1:(0,0,0),
  2:(1,1,0),  3:(1,1,1),
  4:(2,0,0),  5:(2,2,1),  6:(2,2,0),
  7:(3,1,1),  8:(3,1,0),  9:(3,3,1), 10:(3,3,0),
 11:(4,0,0), 12:(4,2,0), 13:(4,2,1), 14:(4,4,0), 15:(4,4,1),
 16:(5,1,0), 17:(5,1,1), 18:(5,3,0), 19:(5,3,1), 20:(5,5,0), 21:(5,5,1),
 22:(6,0,0), 23:(6,2,1), 24:(6,2,0), 25:(6,4,1), 26:(6,4,0), 27:(6,6,1), 28:(6,6,0),
 29:(7,1,1), 30:(7,1,0), 31:(7,3,1), 32:(7,3,0), 33:(7,5,0), 34:(7,5,1), 35:(7,7,0), 36:(7,7,1),
 37:(8,0,0), 38:(8,2,0), 39:(8,2,1), 40:(8,4,0), 41:(8,4,1), 42:(8,6,0), 43:(8,6,1), 44:(8,8,0), 45:(8,8,1),
 46:(9,1,0), 47:(9,1,1), 48:(9,3,0), 49:(9,3,1), 50:(9,5,0), 51:(9,5,1), 52:(9,7,0), 53:(9,7,1), 54:(9,9,0), 55:(9,9,1)
}

def factorial(up_num,low_num=1):
  j=1.0
  for i in range(low_num,up_num+1):
    if i!=0: j=j*i
  return(j+0.0)   

def zernNumToDegFreq(num):
   '''Return the n,m, and even/oddness of a given Zernike number
     as defined in Hardy's "AO for Astronomical Telescope"'''
   if num==0: return([-1,-1,-1])
   target=0
   n=0
   while 1:
      for m in numpy.arange(1+int(n-n%2)/2)*2+(n%2):
         target=target+1
         if target==num: return([n,m,num%2])
         if m!=0:
            target=target+1
            if target==num: return([n,m,num%2])
      n=n+1  

def anyZernike(znum, gridSize, outerRadius=None, ratio=1, ongrid=1, clip=1, verbose=0):
  if outerRadius == None: outerRadius = (gridSize-1.0)/2.0+1.0e-10
  baseRadius = radius(gridSize, gridSize, ratio, ongrid)/outerRadius+0.0 # need double precision
  zern=baseRadius*0.0

  if verbose:
    print("Zernike number %d:" % (znum))

  # extract the core parameters
  n = int(zernNumToDegFreq( znum )[0])
  m = int(zernNumToDegFreq( znum )[1])
  odd = int(zernNumToDegFreq( znum )[2])
  if verbose:
    print("\tn=%d, m=%d, odd=>%d" % (n,m,odd))

  # prepare our r^[n-2S] and cos here
  numr=int(n-m/2)
  etom = expTheta(gridSize, gridSize, ongrid)
  etom = etom**m

  for S in range( int((n-m)/2+1) ):
    coeff=((-1.0)**S)*factorial(n-S) # numerator
    coeff=coeff/(factorial(S) * factorial(int((n+m)/2-S)) * factorial(int((n-m)/2-S)) ) # denominator
    zern=zern+coeff*baseRadius**(n-2*S)
    if verbose:
      print("\tr^%d, coeff = %5.3f" % (n-2*S,coeff))

  if m==0:
    zern=zern*numpy.sqrt(n+1)
  else:
    if odd:
      zern=zern*etom.imag*numpy.sqrt(2*n+2)
    else:
      zern=zern*etom.real*numpy.sqrt(2*n+2)
  if clip: 
     return(zern*numpy.less_equal(baseRadius, 1.0))
  else:
     return(zern)

def radius(xSize, ySize, ratio=1, ongrid=1, offset=None):
    '''Calculate the radius from the centre of a rectangular grid
      ongrid=1 = the coordinates are relative to pixel edges
      ongrdi=0 = the coordinates are relative to pixel centres'''
    if offset == None:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 
       ry = numpy.arange(ySize) - (ySize-ongrid*1.0)/2.0
    elif len(offset)>1:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 - offset[0]
       ry = numpy.arange(ySize) - (ySize-ongrid*1.0)/2.0 - offset[1]
    else:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 - offset
       ry = numpy.arange(ySize) - (ySize-ongrid*1.0)/2.0 - offset
    ry *= ratio # scale
    rxSquared = rx*rx
    rySquared = ry*ry
    rSquared = numpy.add.outer(rySquared,rxSquared)
    return(numpy.sqrt(rSquared))

def radius_coordIndep(coords):
    '''Calculate the radius from a set of coordinates'''
    rxSquared = coords[:,0]**2
    rySquared = coords[:,1]**2
    return(numpy.sqrt(rxSquared**2+rySquared**2))

def angle(xSize, ySize, ongrid=1, offset=None):
    '''Calculate the angle from centre of grid -> row=x, column=y
      and define 0/2pi as along (xSize/2,<any>)'''
    if offset == None:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 
       ry = numpy.reshape( arange(ySize) - (ySize-ongrid*1.0)/2.0 , (-1,1) )
    elif len(offset)>1:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 -offset[0]
       ry = numpy.reshape( arange(ySize) - (ySize-ongrid*1.0)/2.0 , (-1,1) ) -offset[1]
    else:
       rx = numpy.arange(xSize) - (xSize-ongrid*1.0)/2.0 -offset
       ry = numpy.reshape( arange(ySize) - (ySize-ongrid*1.0)/2.0 , (-1,1) ) -offset
    angle = numpy.arctan2(rx, ry)+numpy.pi # +pi so 0 le angle le 2pi
#    if (ySize-ongrid*1.)/2. % 1:
#      angle = where( rx == 0 and ry > 0
    return(angle)

def expTheta(xSize, ySize, ongrid, ratio=1):
    '''Return a rectangular grid containing exp(i*theta), where theta is 
       the angle between the positive x axis and the vector from the centre
       of the grid to each gridpoint'''
    rx = numpy.arange(xSize) - (xSize-1.0*ongrid)/2.0 
    ry = numpy.arange(ySize) - (ySize-1.0*ongrid)/2.0
    cosPart = rx
    sinPart = numpy.reshape(1j*ry, (-1,1))
    self = (cosPart + sinPart)/(1.0e-10 + radius(xSize, ySize, ratio, ongrid))
    return(self)

def expTheta_coordIndep(coords):
    '''Return a set of coordinates containing exp(i*theta), where theta is 
       the angle between the positive x axis and the vector from the centre
       of the grid to each gridpoint'''
    cosPart = coords[:,0]
    sinPart = 1j*coords[:,1]
    self = (cosPart + sinPart)/(1.0e-10 + radius_coordIndep(coords))
    return(self)