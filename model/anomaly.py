import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)


def plot_make_v1(motor_list, csv_list, target, use_method, ori_path, Sampling_sec = 50, plus = 3, minus = 3):
    using_csv = [csv for csv in csv_list if target in csv]
    motor_list = list(map(lambda x: x.split('_')[1],using_csv))

    Norm_min, Norm_max = [], []
    Err_min, Err_max = [], []
    Check_df = pd.DataFrame()
    ori_df = pd.DataFrame()

    plt.figure(figsize=(15, 8))
    count = 0
    Sampling_sec = 50 # 초기 50초 데이터를 이용하여 나머지를 맞춤


    for motor in motor_list:
        count +=1
        motor_check = [csv for csv in csv_list if motor in csv]

        df_list = [csv for csv in csv_list if motor_list[0] in csv]
        if len(motor_check) > 1:
            norm_df = pd.read_csv(ori_path + '3. csv/' + [x for x in motor_check if '정상' in x][0])
            err_df = pd.read_csv(ori_path + '3. csv/' + [x for x in motor_check if target in x][0])
        else:
            continue        
        
        ini_data = norm_df.loc[:50,use_method]
        ini_mean = ini_data.mean()
        # 정상
        Norm_mean = norm_df[use_method].groupby(norm_df[use_method].index//Sampling_sec).mean()
        Norm_mean_check = Norm_mean/ini_mean

        Nc_mean = Norm_mean_check.mean()
        W_p = Nc_mean + np.std(Norm_mean_check) * plus
        W_m = Nc_mean - np.std(Norm_mean_check) * minus

        # 고장
        Err_mean = err_df[use_method].groupby(err_df[use_method].index//Sampling_sec).mean()
        Err_mean_check = Err_mean/ini_mean



        Check_df = pd.concat([Check_df,
                   pd.DataFrame([[motor, min(Norm_mean_check),max(Norm_mean_check), min(Err_mean_check),max(Err_mean_check),W_p,W_m]],
                                columns=['motor', 'Norm_mean/ini', 'Norm_max/ini', 'Err_min/ini', 'Err_max/ini','Error', 'Error-'])
                  ],ignore_index= True)

        state_col = {'정상': 'blue', '베어링불량' : 'orange', "회전체불평형": "green", "축정렬불량": "brown", "벨트느슨함": "dimgrey"}

        plt.subplot(4,4,count)
        plt.plot(Norm_mean_check,label = '정상', color = 'blue')
        plt.plot(Err_mean_check,label = target, color = 'green')
        plt.axhline(Check_df[Check_df['motor']== motor]['Error'].values[0], color = 'black', label = 'Error', linestyle = '--')
        plt.axhline(Check_df[Check_df['motor']== motor]['Error-'].values[0], color = 'black', label = 'Error', linestyle = '--')

        plt.title(motor)
        plt.tight_layout()

    # 라벨만 붙이기
    plt.subplot(4,4,count + 1)
    plt.plot([], [], label="정상", color="blue")  # Add a placeholder plot
    plt.plot([], [], label= target, color="green")  # Add another placeholder plot
    plt.axhline(0, color='black', label='Error', linestyle='--')

    # Remove unnecessary axes
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')  # Hide the axes completely

    # Add the legend
    plt.legend(loc='center', bbox_to_anchor=(0.5, -0.05), ncol=3)  # Adjust position as needed

    plt.show()

    
# 초기 50초 데이터를 이용하여 나머지를 맞춤
def plot_make(motor_list, csv_list, target, use_method, ori_path, Sampling_sec = 50):
    using_csv = [csv for csv in csv_list if target in csv]
    motor_list = list(map(lambda x: x.split('_')[1],using_csv))

    Norm_min, Norm_max = [], []
    Err_min, Err_max = [], []
    Check_df = pd.DataFrame()
    ori_df = pd.DataFrame()

    plt.figure(figsize=(15, 8))
    count = 0
    # Sampling_sec = 50 


    for motor in motor_list:
        count +=1
        motor_check = [csv for csv in csv_list if motor in csv]

        df_list = [csv for csv in csv_list if motor_list[0] in csv]
        if len(motor_check) > 1:
            norm_df = pd.read_csv(ori_path + '3. csv/' + [x for x in motor_check if '정상' in x][0])
            err_df = pd.read_csv(ori_path + '3. csv/' + [x for x in motor_check if target in x][0])
        else:
            continue

        ini_data = norm_df.loc[:50,use_method]
        ini_mean = ini_data.mean()
        # 정상
        Norm_mean = norm_df[use_method].groupby(norm_df[use_method].index//Sampling_sec).mean()
        Norm_mean_check = Norm_mean/ini_mean

        Nc_mean = Norm_mean_check.mean()
        W_1 = Nc_mean + np.std(Norm_mean_check) * 1
        W_2 = Nc_mean + np.std(Norm_mean_check) * 2
        W_3 = Nc_mean + np.std(Norm_mean_check) * 3

        warn_point_1 = ini_mean + np.std(ini_data) *1
        warn_point_2 = ini_mean + np.std(ini_data) *2
        warn_point_3 = ini_mean + np.std(ini_data) *3
        # 고장
        Err_mean = err_df[use_method].groupby(err_df[use_method].index//Sampling_sec).mean()
        Err_mean_check = Err_mean/ini_mean



        Check_df = pd.concat([Check_df,
                   pd.DataFrame([[motor, min(Norm_mean_check),max(Norm_mean_check), min(Err_mean_check),max(Err_mean_check),W_1,W_2,W_3]],
                                columns=['motor', 'Norm_mean/ini', 'Norm_max/ini', 'Err_min/ini', 'Err_max/ini','Warn1','Warn2','Error'])
                  ],ignore_index= True)

        ori_df = pd.concat([ori_df,
                   pd.DataFrame([[motor, min(Norm_mean),max(Norm_mean), min(Err_mean),max(Err_mean)
                                  ,ini_mean, warn_point_1, warn_point_2, warn_point_3]],
                                columns=['motor', 'Norm_mean', 'Norm_max', 'Err_min', 'Err_max','initial value','warn_point_1','warn_point_2','warn_point_3'])
                  ],ignore_index= True)

        state_col = {'정상': 'blue', '베어링불량' : 'orange', "회전체불평형": "green", "축정렬불량": "brown", "벨트느슨함": "dimgrey"}

        plt.subplot(4,4,count)
        plt.plot(Norm_mean_check,label = '정상', color = 'blue')
        plt.plot(Err_mean_check,label = target, color = 'green')
        # plt.axhline(Check_df[Check_df['motor']== motor]['Warn1'].values[0], color = 'r', label = 'warn1', linestyle = '--')
        plt.axhline(Check_df[Check_df['motor']== motor]['Warn2'].values[0], color = 'yellow', label = 'warn2', linestyle = '--')
        # plt.axhline(Check_df[Check_df['motor']== motor]['Error'].values[0], color = 'black', label = 'Error', linestyle = '--')

        # plt.axhline(ori_df[ori_df['motor'] == motor]['warn_point_2'].values[0], color = 'yellow', label = 'warn2', linestyle = '--')
        # plt.axhline(ori_df[ori_df['motor'] == motor]['warn_point_3'].values[0], color = 'black', label = 'Error', linestyle = '--')
        # plt.axhline(ori_df[ori_df['motor'] == motor]['Norm_max'].values[0], color = 'red')
        plt.title(motor)
        plt.tight_layout()

    # 라벨만 붙이기
    plt.subplot(4,4,count + 1)
    plt.plot([], [], label="정상", color="blue")  # Add a placeholder plot
    plt.plot([], [], label= target, color="green")  # Add another placeholder plot
    # plt.axhline(0, color='r', label='warn1', linestyle='--')  # Add lines for clarity
    # plt.axhline(0, color='yellow', label='warn2', linestyle='--')
    plt.axhline(0, color='black', label='Error', linestyle='--')

    # Remove unnecessary axes
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')  # Hide the axes completely

    # Add the legend
    plt.legend(loc='center', bbox_to_anchor=(0.5, -0.05), ncol=3)  # Adjust position as needed

    plt.show()

    