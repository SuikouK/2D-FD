#------------------------#
# 2D-FD ver 1.0          #
# mainModule             #
# author:Kazumi Ishiwata #
#------------------------#
import keyboard          as kb
import numpy             as np
import matplotlib.pyplot as plt
import parameters        as pm
import functions         as fc
import terms             as tm
import warnings
warnings.simplefilter('error')

#シミュレーション本体
def main():
        ims = [] #フィルム

        fc.initMarker()     #設定ファイルから読み込んだマーカーを配置する
        fc.initRandMarker() #ランダムなマーカーを配置する
        
        try:
                if pm.command_stop:
                        print('E長押しで計算を終了します')
                for nt in range(pm.nt):
                        print(str(nt + 1) + ' / ' + str(pm.nt) + '  t = ' + str(pm.t) + 's') #進捗表示

                        #録画(1枚分)
                        if nt % (pm.spf / pm.dt) == 0:
                                fc.drawScreen()
                                fc.logImage(ims,pm.drawing_mode,pm.t,ax,pm.ny)
                        
                        #計算
                        pm.t += pm.dt #時刻

                        pm.ux[1:-1,1:-1] = (pm.ux[1:-1, 1:-1] + tm.advectionTerm('x') + tm.viscosityTerm('x') + tm.pressureTerm('x') + pm.Kx[1:-1,1:-1] * pm.dt) #流速
                        pm.uy[1:-1,1:-1] = (pm.uy[1:-1, 1:-1] + tm.advectionTerm('y') + tm.viscosityTerm('y') + tm.pressureTerm('y') + pm.Ky[1:-1,1:-1] * pm.dt)
                        
                        fc.setBC() #境界条件

                        tm.solvePressure() #圧力

                        fc.drawMarker() #マーカー

                        #E長押しで計算中断
                        if pm.command_stop and kb.is_pressed('e'):
                                pm.result_all = 't = ' + str(pm.t) + ' で計算終了コマンドを検出しました。'
                                break
                if nt + 1 == pm.nt:
                        pm.result_all = ' 計算は正常に終了しました。'
        except RuntimeWarning:
                pm.result_all = 't = ' + str(pm.t) + 'で解が発散しました。'
        except:
                pm.result_all = 't = ' + str(pm.t) + 'でエラーが発生しました。'
        finally: #エラーが発生しても結果は出力する
                print(pm.result_all)
                fc.drawScreen()
                fc.logImage(ims,pm.drawing_mode,pm.t,ax,pm.ny)
                #計算結果を元にアニメーションを作成
                fc.makeAnime(fig,ims,pm.spf,pm.drawing_mode)
                fc.showMarker('dot')
                pm.writeResult() #結果をconfig.xlsxに書き込み
                print('complete.') #進捗表示

#グラフの設定
fig,ax = plt.subplots()
ax.set_xlim(0, pm.nx - 1) #描画範囲
ax.set_ylim(0, pm.ny - 1)
ax.set_xlabel("x [m]", fontsize = 10) #軸ラベル
ax.set_ylabel("y [m]", fontsize = 10)
x_metric = fc.setMetric(pm.x_min,pm.x_max) #[m] 軸目盛間隔
y_metric = x_metric                        #[m]
start,end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start,end,x_metric / pm.dx))
start,end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start,end,y_metric / pm.dy))
ax.set_xticklabels(np.round(np.arange(pm.x_min,pm.x_max,x_metric),1)) #軸目盛り
ax.set_yticklabels(np.round(np.arange(pm.y_min,pm.y_max,y_metric),1))
#ax.grid() #格子

#シミュレーション実行
if __name__ == "__main__":
    main()