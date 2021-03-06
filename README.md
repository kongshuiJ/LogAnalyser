## 注意事项：
1. 解析log功能和解析pmap文件功能可以一起使用，但不推荐；
2. 软件界面"系统级"中
- "[D]: debug"
- "[I]: info"
- "[E]: error"
- "[W]: warn"
3. 软件界面"user level"功能必须由编写好的json文件支持，正常情况json文件内容应该由相关模块的开发人员提前编写；
4. 使用者必须确定点击的某个"user level"是属于哪一个"system level"(就是说属于的log级别)，只有在所属的"system level"被按下后，才会显示出正确的"user level"的内容。


## 软件正常模式解析log文件使用说明:
1. 开启软件：
        移动到"loganalyser/src"目录下执行"sudo python3 gui.py"
    
2. 加载log文件：
    1. 菜单栏点击"files"，双击"open log file"
    
3. 查看正则表达式过滤出来的log信息：
    1. 确保有json文件后，在选择好"system level"的前提下，进行选择"user level"；

4. 已显示log信息的情况下进行关键词搜索
    1. 选择好"user level"和"system level"，并且软件上方输出框显示出正确的log信息；
    2. 在"base64"标题下的输入框输入关键词，软件会在上方输出框显示的log信息中寻找含有关键词的句子，并且打印在标题为"Filtered information"的下方。


## 软件便捷模式解析log文件使用说明(方便不了解编写json文件的使用者)：
1. 按照"软件正常模式解析log文件使用说明"开启软件并且加载log文件；
2. 点击菜单栏"quick view"中的"log file"，弹出一个新窗口；


## 分析pmap文件使用说明：
1. 开启软件；
2. 菜单栏点击"files"，双击"open pmap file"；
3. 确认文件后，解析出来的内容会打印在标题为"Filtered information"的下方。


## 软件便捷模式查看Ayla指令使用说明：
1. 按照"软件正常模式解析log文件使用说明"开启软件并且加载log文件；
2. 点击菜单栏"quick view"中的"Ayla instruction"，弹出一个新窗口；
3. 在弹出的新窗口中，可以看到每一个Ayla指令的执行时间和译文。
 
