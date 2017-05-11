def boundarycheck(i, j, (Vx, Vy)):
    # if value is equal to zero then position  is no boundary
    # if value is not equal to zero then position is a boundary
    if Vx[i][0] != 0 or Vx[i][1] != 0 or Vy[j][0] != 0 or Vy[j][1] != 0:
        if i == 0 or j == 0 or i == len(Vx) - 1 or j == len(Vy) - 1:

            check = True
        elif Vx[i - 1][0] != 0 or Vx[i - 1][1] != 0 or Vy[j - 1][0] != 0 or Vy[j - 1][1] != 0:
            if Vx[i + 1][0] == 0 and Vx[i + 1][1] == 0 or Vy[j + 1][0] == 0 and Vy[j + 1][1] == 0:
                check = True
            else:
                check = False
        elif Vx[i - 1][0] == 0 or Vx[i - 1][1] == 0 or Vy[j - 1][0] == 0 or Vy[j - 1][1] == 0:
            if Vx[i + 1][0] != 0 or Vx[i + 1][1] != 0 or Vy[j + 1][0] != 0 or Vy[j + 1][1] != 0:
                check = True
            elif Vx[i + 1][0] == 0 and Vx[i + 1][1] == 0 or Vy[j + 1][0] == 0 and Vy[j + 1][1] == 0:
                check = True
            else:
                check = False
    else:
        check = False
    return check
