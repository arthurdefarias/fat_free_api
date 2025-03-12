import math

pi = math.pi

area_interna = pi * ((0.3228 - 2*0.0150) / 2) ** 2

area_steel = pi * (((0.3228) / 2) ** 2 - ((0.3228 - 2*0.0150)/ 2) ** 2)
area_concrete = pi * (((0.3228+2*0.010) / 2) ** 2 - ((0.3228)/ 2) ** 2)
area_coating = pi * (((0.3228+2*0.010+2*0.003) / 2) ** 2 - ((0.3228+2*0.010)/ 2) ** 2)

area_externa = pi * (((0.3228+2*0.010+2*0.003) / 2) ** 2)


print('area interna '  + str(area_interna))
print('area steel ' + str(area_steel))
print('area coating ' + str(area_coating))
print('area concrete ' + str(area_concrete))
print('soma ' + str(area_interna + area_steel +  area_coating + area_concrete))
print('area externa ' + str(area_externa))