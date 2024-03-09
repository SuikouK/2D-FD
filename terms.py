#------------------------#
# 2D-FD ver 1.0          #
# terms                  #
# author:Kazumi Ishiwata #
#------------------------#
import parameters as pm
import functions  as fc

#移流項(後方差分法)
def advectionTerm(x_or_y :str):
    if x_or_y == 'x':
        return - (  pm.ux[1:-1, 1:-1] * pm.dt / pm.dx * (pm.ux[1:-1, 1:-1] - pm.ux[0:-2,1:-1])
                  + pm.uy[1:-1, 1:-1] * pm.dt / pm.dy * (pm.ux[1:-1, 1:-1] - pm.ux[1:-1,0:-2]) )
    if x_or_y == 'y':
        return - (  pm.ux[1:-1, 1:-1] * pm.dt / pm.dy * (pm.uy[1:-1, 1:-1] - pm.uy[0:-2,1:-1])
                  + pm.uy[1:-1, 1:-1] * pm.dt / pm.dx * (pm.uy[1:-1, 1:-1] - pm.uy[1:-1,0:-2]) )

#粘性項(陽解法)
def viscosityTerm(x_or_y :str):
    if x_or_y == 'x':
        return pm.nu * (  pm.dt / pm.dx**2 * (pm.ux[2:,1:-1] - 2 * pm.ux[1:-1, 1:-1] + pm.ux[:-2,1:-1])
                        + pm.dt / pm.dy**2 * (pm.ux[1:-1,2:] - 2 * pm.ux[1:-1, 1:-1] + pm.ux[1:-1,:-2]) )
    if x_or_y == 'y':
        return pm.nu * (  pm.dt / pm.dy**2 * (pm.uy[2:,1:-1] - 2 * pm.uy[1:-1, 1:-1] + pm.uy[:-2,1:-1])
                        + pm.dt / pm.dx**2 * (pm.uy[1:-1,2:] - 2 * pm.uy[1:-1, 1:-1] + pm.uy[1:-1,:-2]) )

#圧力項(中心差分法)
def pressureTerm(x_or_y :str):
    if x_or_y == 'x':
        return - pm.dt / (2 * pm.ro * pm.dx) * (pm.p[2:,1:-1] - pm.p[:-2,1:-1])
    if x_or_y == 'y':
        return - pm.dt / (2 * pm.ro * pm.dy) * (pm.p[1:-1,2:] - pm.p[1:-1,:-2])

#圧力(ヤコビの反復法)
def solvePressure():
    b_solve()
    for i in range(pm.n_psolve):
        p_old = pm.p.copy()
        pm.p[1:-1, 1:-1] = ((  (p_old[1:-1, 2:] + p_old[1:-1, 0:-2]) * pm.dy**2 
                             + (p_old[2:, 1:-1] + p_old[0:-2, 1:-1]) * pm.dx**2 )
                             / (2 * (pm.dx**2 + pm.dy**2))
                            - pm.dx**2 * pm.dy**2 / (2 * (pm.dx**2 + pm.dy**2)) 
                            * pm.b[1:-1,1:-1])
        if pm.x_bc == 'periodic':
            fc.periBC_x(pm.p )
        if pm.y_bc == 'periodic':
            fc.periBC_y(pm.p )
        fc.setBarrierBC_p()

#圧力に関するポアソン方程式のソース項(中心差分法)
def b_solve():
    pm.b[1:-1, 1:-1] = (pm.ro * (1 / pm.dt * 
                       ((pm.ux[2:,1:-1] - pm.ux[:-2,1:-1]) / 
                        (2 * pm.dx) + (pm.uy[1:-1,2:] - pm.uy[1:-1,:-2]) / (2 * pm.dy)) -
                       ((pm.ux[2:,1:-1] - pm.ux[:-2,1:-1]) / (2 * pm.dx))**2 -
                         2 * ((pm.ux[1:-1,2:] - pm.ux[1:-1,:-2]) / (2 * pm.dy) *
                              (pm.uy[2:,1:-1] - pm.uy[:-2,1:-1]) / (2 * pm.dx))-
                             ((pm.uy[1:-1,2:] - pm.uy[1:-1,:-2]) / (2 * pm.dy))**2))