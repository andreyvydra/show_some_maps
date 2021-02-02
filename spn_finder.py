def get_spn(point1, point2):
    spn_x = abs(point1[0] - point2[0]) / 2
    spn_y = abs(point1[1] - point2[1]) / 2
    return ','.join([str(spn_x), str(spn_y)])
