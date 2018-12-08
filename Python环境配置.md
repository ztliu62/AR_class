# Windows下的Python环境配置
第一步：首先从官网安装[Anaconda](https://www.anaconda.com/download/#windows)，可以参考[帖子](https://www.jianshu.com/p/cd35110f1ed0)

第二步：通过运行打开windows中的cmd，在其中输入
```
conda env create -f CompPoto.yml
```
此时程序将开始安装课程所需要的Python库文件

第三步：可以通过以下命令激活实验环境
```
activate CompPhoto
```
第四步：运行测试脚本
```
python envTestify.py
```
如果测试运行成功，则可以进一步进行实验；

如果系统报错没有找到OpenCV库文件，则需要进一步运行
```
conda install -c menpo opencv
```
来完成对OpenCV的手动安装
