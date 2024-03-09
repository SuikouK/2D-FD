#------------------------#
# 2D-FD ver 1.0          #
# functions              #
# author:Kazumi Ishiwata #
#------------------------#
import matplotlib.animation as ani
import matplotlib.pyplot    as plt
import numpy                as np
import random               as rd
import seaborn              as sns
import parameters           as pm

#計算領域端の境界条件をセットする
def setBC() -> None:
    if pm.x_bc == 'periodic': #周期的境界条件(x方向)
        periBC_x(pm.ux)
        periBC_x(pm.uy)
        periBC_x(pm.p )
    elif pm.x_bc == 'free':   #自由境界条件(x方向)
        freeBC_x(pm.ux)
        freeBC_x(pm.uy)
        freeBC_x(pm.p )
    elif pm.x_bc == 'const':   #固定境界条件(x方向)
        pass
    if pm.y_bc == 'periodic':  #周期的境界条件(y方向)
        periBC_y(pm.ux)
        periBC_y(pm.uy)
        periBC_y(pm.p )
    elif pm.y_bc == 'free':   #自由境界条件(y方向)
        freeBC_y(pm.ux)
        freeBC_y(pm.uy)
        freeBC_y(pm.p )
    elif pm.y_bc == 'const':   #固定境界条件(y方向)
        pass
    setBarrierBC_u()
    setBarrierBC_p()

#周期的境界条件(x方向)
def periBC_x(mat :np.ndarray) -> None:
    mat_old = mat.copy()
    mat[0   ,1:-1] = mat_old[  -2,1:-1]
    mat[  -1,1:-1] = mat_old[1   ,1:-1]

#周期的境界条件(y方向)
def periBC_y(mat :np.ndarray) -> None:
    mat_old = mat.copy()
    mat[1:-1,  -1] = mat_old[1:-1,1   ]
    mat[1:-1,0   ] = mat_old[1:-1,  -2]

#自由境界条件(x方向)
def freeBC_x(mat :np.ndarray) -> None:
    mat_old = mat.copy()
    mat[0   ,1:-1] = mat_old[1   ,1:-1]
    mat[  -1,1:-1] = mat_old[  -2,1:-1]

#自由境界条件(y方向)
def freeBC_y(mat :np.ndarray) -> None:
    mat_old = mat.copy()
    mat[1:-1,  -1] = mat_old[1:-1,  -2]
    mat[1:-1,0   ] = mat_old[1:-1,1   ]

#流速の壁境界条件をセットする
def setBarrierBC_u() -> None:
    pm.ux = (np.ones((pm.nx, pm.ny)) - pm.barrier) * pm.ux
    pm.ux[1:-1,1:-1] = (  pm.ux[1:-1,1:-1]
                      + ( pm.w_l[1:-1,1:-1]  * pm.ux[  :-2, 1:-1]
                        + pm.w_r[1:-1,1:-1]  * pm.ux[ 2:  , 1:-1]
                        + pm.w_d[1:-1,1:-1]  * pm.ux[ 1:-1,  :-2]
                        + pm.w_u[1:-1,1:-1]  * pm.ux[ 1:-1, 2:  ]
                        + pm.e_ld[1:-1,1:-1] * pm.ux[  :-2,  :-2]
                        + pm.e_lu[1:-1,1:-1] * pm.ux[  :-2, 2:  ]
                        + pm.e_rd[1:-1,1:-1] * pm.ux[ 2:  ,  :-2]
                        + pm.e_ru[1:-1,1:-1] * pm.ux[ 2:  , 2:  ]) * 0.5)

    pm.uy = (np.ones((pm.nx, pm.ny)) - pm.barrier) * pm.uy
    pm.uy[1:-1,1:-1] = (  pm.uy[1:-1,1:-1]
                      + ( pm.w_l[1:-1,1:-1]  * pm.uy[  :-2, 1:-1]
                        + pm.w_r[1:-1,1:-1]  * pm.uy[ 2:  , 1:-1]
                        + pm.w_d[1:-1,1:-1]  * pm.uy[ 1:-1,  :-2]
                        + pm.w_u[1:-1,1:-1]  * pm.uy[ 1:-1, 2:  ]
                        + pm.e_ld[1:-1,1:-1] * pm.uy[  :-2,  :-2]
                        + pm.e_lu[1:-1,1:-1] * pm.uy[  :-2, 2:  ]
                        + pm.e_rd[1:-1,1:-1] * pm.uy[ 2:  ,  :-2]
                        + pm.e_ru[1:-1,1:-1] * pm.uy[ 2:  , 2:  ]) * 0.5)

#圧力の壁境界条件をセットする
def setBarrierBC_p() -> None:
    pm.p = (np.ones((pm.nx, pm.ny)) - pm.w_all) * pm.p
    pm.p[1:-1,1:-1] = (  pm.p[1:-1,1:-1]
                        + pm.w_l[1:-1,1:-1]  * pm.p[  :-2, 1:-1]
                        + pm.w_r[1:-1,1:-1]  * pm.p[ 2:  , 1:-1]
                        + pm.w_d[1:-1,1:-1]  * pm.p[ 1:-1,  :-2]
                        + pm.w_u[1:-1,1:-1]  * pm.p[ 1:-1, 2:  ]
                        + pm.e_ld[1:-1,1:-1] * pm.p[  :-2,  :-2]
                        + pm.e_lu[1:-1,1:-1] * pm.p[  :-2, 2:  ]
                        + pm.e_rd[1:-1,1:-1] * pm.p[ 2:  ,  :-2]
                        + pm.e_ru[1:-1,1:-1] * pm.p[ 2:  , 2:  ])

#格子インデックスから位置を求める
def pos(x_or_y :str,idx :int) -> float:
    if x_or_y == 'x':
        return (idx + 0.5) * pm.dx + pm.x_min
    if x_or_y == 'y':
        return (idx + 0.5) * pm.dy + pm.y_min

#位置から格子インデックスを求める
def idx(x_or_y :str,pos :float) -> int:
    if x_or_y == 'x':
        return int((pos - pm.x_min)/ pm.dx)
    if x_or_y == 'y':
        return int((pos - pm.y_min)/ pm.dy)

#位置(x,y)のマーカーを作る
def createMarker(x :float,y :float) -> None:
    pm.marker_x.append(x)
    pm.marker_y.append(y)

#i番目のマーカーを消す
def deleteMarker(i :int) -> None:
    pm.marker_x.pop(i)
    pm.marker_y.pop(i)

#全てのマーカーを消す
def deleteAllMarker() -> None:
    pm.marker_x = []
    pm.marker_y = []

#マーカーの初期化
def initMarker() -> None:
    for i in range(pm.nx):
        for j in range(pm.ny):
            if pm.marker_scr_first[i,j] == 1:
                createMarker(pos('x',i),pos('y',j))

#ランダムマーカーの配置  
def initRandMarker() -> None: 
    if pm.random_marker == True:
        i :int = 0
        while(i < pm.numOfmarker):
            marker_x_pre = pm.x_min + (pm.x_max - pm.x_min) * rd.random()
            idx_marker_x = idx('x',marker_x_pre)
            marker_y_pre = pm.y_min + (pm.y_max - pm.y_min) * rd.random()
            idx_marker_y = idx('y',marker_y_pre)
            if pm.barrier[idx_marker_x,idx_marker_y] == 0:
                createMarker(marker_x_pre,marker_y_pre)
                i = i + 1

#マーカーの運動を描く
def drawMarker() -> None:
    if   pm.drawing_mode == 'stream line':
        drawStreamline()
    elif pm.drawing_mode == 'streak line':
        drawStreakline()
    else:
        drawDotOrPastline(pm.drawing_mode)

#dotか流跡線を描く
def drawDotOrPastline(mode :str) -> None:
    frameWidth :int = 1 #枠外の幅 / dx or dy
    i :int = 0
    while(i < len(pm.marker_x)):
        nx = int((pm.marker_x[i] - pm.x_min)/ pm.dx)
        ny = int((pm.marker_y[i] - pm.y_min)/ pm.dy)
        marker_xfut = pm.marker_x[i] + pm.ux[nx,ny] * pm.dt
        marker_yfut = pm.marker_y[i] + pm.uy[nx,ny] * pm.dt

        if marker_xfut <= pm.x_min + frameWidth * pm.dx: #周期的境界条件のとき、範囲外に出たマーカーは反対側から戻す(x方向)
            if pm.x_bc == 'periodic':
                pm.marker_x[i] = pm.x_max - frameWidth * pm.dx
            else:
                deleteMarker(i)
                continue
        if marker_xfut >= pm.x_max - frameWidth * pm.dx:
            if pm.x_bc == 'periodic':
                pm.marker_x[i] = pm.x_min + frameWidth * pm.dx
            else:                                        #周期的境界条件でないとき、範囲外に出たマーカーは削除する(x方向)
                deleteMarker(i)
                continue
        else:
            pm.marker_x[i] = marker_xfut

        if marker_yfut <= pm.y_min + frameWidth * pm.dy: #周期的境界条件のとき、範囲外に出たマーカーは反対側から戻す(y方向)
            if pm.y_bc == 'periodic':
                pm.marker_y[i] = pm.y_max - frameWidth * pm.dy
            else:
                deleteMarker(i)
                continue
        if marker_yfut >= pm.y_max - frameWidth * pm.dy:
            if pm.y_bc == 'periodic':
                pm.marker_y[i] = pm.y_min + frameWidth * pm.dy
            else:                                        #周期的境界条件でないとき、範囲外に出たマーカーは削除する(y方向)
                deleteMarker(i)
                continue
        else:
            pm.marker_y[i] = marker_yfut

        i = i + 1
    showMarker(mode)

#流線を描く
def drawStreamline() -> None:
    pm.marker_scr = pm.barrier * pm.show_barrier
    i :int = 0
    while(i < 15 * max(pm.nx,pm.ny) and len(pm.marker_x) != 0):
        drawDotOrPastline('pastLine')
        i = i + 1
    deleteAllMarker()
    initMarker()

#流脈線を描く
def drawStreakline() -> None:
    for i in range(pm.nx):
        for j in range(pm.ny):
            if pm.marker_scr_first[i,j] == 1:
                createMarker(pos('x',i),pos('y',j))
    drawDotOrPastline('dot')

#マーカーをスクリーンに映す
def showMarker(mode :str) -> None:
    if mode == 'dot':
        pm.marker_scr = pm.barrier * pm.show_barrier
    for i in range(len(pm.marker_x)):
        idx_x = idx('x',pm.marker_x[i])
        idx_y = idx('y',pm.marker_y[i])
        if 0 <= idx_x <= pm.nx and 0 <= idx_y <= pm.ny:
            pm.marker_scr[idx_x,idx_y] = 1        #バイナリ
            #pm.marker_scr[idx_x,idx_y] = i * 0.05 #カラフル

#ヒートマップを保存する(未完成)
def makeFig(mat :np.ndarray,colmap :str,fileName :str) -> None:
    plt.figure()
    #sns.heatmap(np.flipud(mat.T),cbar=False,square=True)
    sns.heatmap(mat.T ,cbar = False ,square = True ,cmap = colmap)
    #ax.invert_yaxis()
    plt.savefig(fileName)
    return

#目盛間隔を調整する
def setMetric(x_min,x_max) -> float:
    x_range = x_max - x_min
    metrix = ( (0.05,0.1,0.2,0.5,  1,  2,  5, 10, 20, 50, 100, 200, 500), 
               ( 0.2,0.5,  1,  2,  5, 10, 20, 50,100,200, 500,1000,2000), 
               ( 0.5,  1,  2,  5, 10, 20, 50,100,200,500,1000,2000,5000) )
    for idx in range(len(metrix[0])):
        if x_range > metrix[1][idx] and x_range <= metrix[2][idx]:
            x_metric = metrix[0][idx];break
        else:
            x_metric = 1000
    return x_metric

#screenの更新
def drawScreen():
    if (pm.drawing_mode == 'dot'         or 
        pm.drawing_mode == 'past line'   or
        pm.drawing_mode == 'stream line' or
        pm.drawing_mode == 'streak line'   ):
        pm.screen = pm.marker_scr
    if  pm.drawing_mode == 'p':
        pm.screen = pm.p
    if  pm.drawing_mode == 'kinetic energy':
        pm.screen = pm.ux * pm.ux + pm.uy * pm.uy
    if  pm.drawing_mode == 'vorticity':
        pm.screen[1:-1,1:-1] = ( (pm.uy[2:,1:-1] - pm.uy[:-2,1:-1]) / (2 * pm.dx)
                                -(pm.ux[1:-1,2:] - pm.ux[1:-1,:-2]) / (2 * pm.dy) )

#1コマ分録画
def logImage(ims,title,t,ax,ny):
    im = plt.imshow(pm.screen.T, animated=True,cmap=pm.colormap) #計算結果を描画
    timeStamp = ax.text(0, ny + 0.05, title + '  t = {}s'.format(round(t, 3)), fontsize=10) #時刻を記録
    ims.append([im,timeStamp]) #計算結果を記録

#計算結果を元にアニメーションを作成
def makeAnime(fig,ims,spf,fileName):
    print('animation making,') #進捗表示
    #plt.colorbar(aspect=40, pad=0.08, shrink=0.6,orientation='vertical') #カラーバー
    anim = ani.ArtistAnimation(fig, ims, interval= 1000 * spf, blit=True, repeat_delay=0) #インスタンス作成
    anim.save(pm.dirName + '\\02_Process\\' + fileName + '.gif', writer="pillow") #アニメをgifとして保存
    '''print('animation printing,') #進捗表示
    plt.show() #アニメを表示'''
    print('animation complete.') #進捗表示