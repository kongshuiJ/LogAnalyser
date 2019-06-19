#!/usr/bin/python3

SFMList = ["整体分析", "状态分析", "错误分析", "语音分析", "按键分析"]

stateDict = {'WAITING':'等待', 'CLEANING':'清扫', 'DOCKING':'回充', 'PAUSE':'暂停', 
             'ERROR':'错误', 'REMOTE':'遥控', 'SLEEPING':'睡眠', 'SPOTING':'定点清扫',
             'UPDATING':'升级', 'WIFI_CONFIG':'配置网络', 'CHARGING':'充电',
             'BATTERY_FULL':'充电满', 'CLEAN_ZONE':'划区清扫', 'FACTORY_TEST':'老化测试'}

errorDict = {'ERROR_INIT_WIFI':'Wifi初始化失败', 'ERROR_INIT_IMU':'IMU初始化失败','ERROR_INIT_CAM':'CAMERA初始化失败',
             'ERROR_INIT_RVC':'RVC初始化错误', 'ERROR_DATA_ENCODER':'编码器错误','ERROR_DATA_HALL':'霍尔传感器错误',
             'ERROR_DATA_IR':'沿墙传感器错误', 'ERROR_DATA_CLIFF':'地检传感器错误','ERROR_DATA_BUMPER':'碰撞传感器错误',
             'ERROR_DATA_IMU':'IMU数据错误', 'ERROR_DATA_CAM':'CAMERA数据错误','ERROR_DATA_TOF':'沿墙数据错误',
             'ERROR_DATA_RVC':'RVC数据错误', 'ERROR_WHEEL_DROP_L':'左轮悬空错误','ERROR_WHEEL_DROP_R':'右轮悬空错误',
             'ERROR_WHEEL_STUCK_L':'左驱动轮卡死错误', 'ERROR_WHEEL_STUCK_R':'右驱动轮卡死错误','ERROR_FAN_STUCK':'风机错误',
             'ERROR_FAN_BROCKEN':'风机损坏', 'ERROR_SIDE_BRUSH_STUCK_L':'左边刷卡死错误','ERROR_SIDE_BRUSH_STUCK_R':'右边刷卡死错误',
             'ERROR_ROLL_BRUSH_STUCK':'滚刷卡死错误', 'ERROR_VIBRATOR_MOTOR_STUCK':'震动电机错误','ERROR_PUMP_STUCK':'水箱电机卡住',
             'ERROR_SIDE_BRUSH_BROCKEN':'边刷损坏', 'ERROR_ROLL_BRUSH_BROCKEN':'滚刷损坏','ERROR_BUTTON_BROCKEN':'按钮损坏',
             'ERROR_PUMP_BROCKEN':'水泵损坏', 'ERROR_BATTERY_ABNORMAL':'电池错误','ERROR_BATTERY_CRITICAL_LOW':'电池电量过低',
             'ERROR_BATTERY_LOW_TO_START':'电量过低无法清扫', 'ERROR_CHARGE_VOL_ABNORMAL':'充电电压异常','ERROR_TEMPERATURE_HIGH':'温度过高',
             'ERROR_TEMPERATURE_LOW':'温度过低', 'ERROR_DUST_UNINSTALLED':'尘盒未安装','ERROR_TANK_UNINSTALLED':'未安装水箱',
             'ERROR_BASE_DOCK_FAILED':'精对准回充失败', 'ERROR_NO_DOCK_SIGNAL':'未收到回充座信号','ERROR_ATTITUDE':'姿态错误',
             'ERROR_CANNOT_FINISH_CLEAN':'清扫无法完成', 'ERROR_WIFI_CONFIG_TIMEOUT':'WIFI设置超时','ERROR_WIFI_AUTH_FAILED':'WIFI密码错误',
             'ERROR_OTA_FAILED':'升级失败', 'ERROR_OTA_DOWNLOAD_FAILED':'下载错误','ERROR_OTA_NO_SPACE_LEFT':'空间不足',
             'ERROR_OTA_BATTERY_LOW':'升级电量不足', 'ERROR_WIFI_SSID_NOT_FOUND':'未找到SSID','ERROR_WIFI_NO_INTERNET':'WIFI无网络',
             'ERROR_WIFI_NO_SERVICE':'WIFI无服务', 'ERROR_CLIFF_START_FAIL':'悬崖触发无法清扫','ERROR_WHEEL_DROP_START_FAIL':'轮子抬起无法清扫',
             'ERROR_BUMPER_START_FAIL':'碰撞触发无法清扫', 'ERROR_PP_FATAL':'PP错误','ERROR_PP_ESCAPE_FAILED':'脱困失败',
             'ERROR_PP_CANNOT_REACH_DEST':'无法到达目标', 'ERROR_SPOT_ON_DOCKER':'充电桩局部清扫错误','ERROR_AED_NOT_FOUND':'无法找到AED充电桩',
             'ERROR_AED_PROC_STUCK':'无法完成AED', 'ERROR_ROBOT_STUCK':'机器卡住','ERROR_BOUNDARY':'延边错误',
             'ERROR_VT_FATAL':'VT错误', 'ERROR_VT_SLIP':'打滑错误','ERROR_MAP_INCONSISTENT':'地图不一致',
             'ERROR_MAP_BUSY':'存取地图忙', 'ERROR_MAP_IO_ERROR':'存取地图错误', 'ERROR_MAP_NO_SPACE_LEFT':'存地图空间不足',
             'ERROR_MAP_RELOC_FAILED':'重定位失败'}

ctrDict = {'USR_CTR_UP':'前进', 'USR_CTR_DOWN':'后退','USR_CTR_LEFT':'左转','USR_CTR_RIGHT':'右转','USR_CTR_POWER_ON':'开机',
	   'USR_CTR_POWER_OFF':'关机', 'USR_CTR_POWER_ONOFF':'开关机', 'USR_CTR_PAUSE':'暂停','USR_CTR_RESUME':'恢复',
	   'USR_CTR_PAUSE_RESUME':'暂停恢复','USR_CTR_AUTO':'清扫','USR_CTR_STOP':'停止', 'USR_CTR_AUTO_STOP':'清扫停止', 
	   'USR_CTR_SNAKE':'弓字型清扫','USR_CTR_ALONG_WALL':'沿墙','USR_CTR_DOCK':'回充','USR_CTR_WIFI_RESET':'配网',
           'USR_CTR_MUTE':'静音模式', 'USR_CTR_GALE':'强力模式','USR_CTR_SET_SCHEDULE':'设置定时','USR_CTR_OTA':'升级指令',
	   'USR_CTR_CLEAN_ZONE':'画区清扫','USR_CTR_REBOOT':'重启', 'USR_CTR_POWEROFF_IN_STATION':'充电桩上关机', 
	   'USR_CTR_EN_TEST':'进入测试','USR_CTR_EX_TEST':'退出测试','USR_CTR_SLEEP':'休眠','USR_CTR_FACTORY_TEST':'跑机测试',
	   'USR_CTR_BASE_DOCK':'精对准回充', 'USR_CTR_AED':'倒垃圾', 'USR_CTR_AGING_TEST':'老化测试','USR_CTR_RESET':'重置',
	   'USR_CTR_CALI_IMU':'IMU校准'}


# 设置字体大小
def setFont(fontSize):
    return ("Times New Roman", fontSize, "bold")


def getSFMList():
    return SFMList


def getErrorDict():
    return errorDict


def getStateDict():
    return stateDict


def getCtrDict():
    return ctrDict


# 检测字符串是否只包含某些字符串
def checkStrComposition(checkedStr, letterList):
    for letter in checkedStr:
        if not letterList.count(letter):
            return False

    return True
