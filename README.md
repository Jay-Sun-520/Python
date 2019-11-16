# Python
<p>可以在电脑和手机上运行
<p>1. 在电脑上运行要把代码中的"/'改为"\\"
<p>2. 在手机上运行需要装:Termux，依赖库为:itchat
<p>在手机上运行的方法
<p>a. 将文件拷贝至手机内存中的download文件夹下，
<p>b. Termux运行时的库的安装位置为:/data/data/usr/local/lib/python3.5/dist-packages/itchat/utils.py(注意: data/data是隐藏文件夹，看不到的，需要在Termux中用cd命令一层一层进去,cd ls pwd命令都很好用)
<p>b.1 可以在termux中用命令python进入python环境，然后用命令:import site; site.getsitepackages()查看当前在手机中的目录
<p>b.2 进去后按https://blog.csdn.net/yinkaishikd/article/details/86679761 这个网页的方法修改文件，注意random随机文件名可以直接固定，有可能报错。
<p>b.3 进入到手机本文件中的目录
<p>b.4 在手机中用python运行本程序，会在手机文件中的目录下生成QR.png文件，在电脑中打开扫描即可登录运行了
