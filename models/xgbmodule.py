import pandas as pd
import xgboost as xgb
from typing import Union


class FantasyBoost:

    def __init__(self, player_name: str, player_pos: str):
        self.player_name, self.seasonal_data, self.x, self.regressor = None, None, None, None
        self.change(player_name, player_pos)

    def change(self, player_name: str, player_pos: str):
        self.player_name = player_name
        player_pos = player_pos.upper()

        if player_pos == 'QB':
            self.__get_qb()  # self.seasonal_data gets updated within this function
            # self.seasonal_data.to_csv('jalen_hurts.csv')
        elif player_pos == 'RB':
            self.__get_rb_wr(flag=0)
        elif player_pos == 'WR':
            self.__get_rb_wr(flag=1)
        elif player_pos == 'TE':
            self.__get_te()
        elif player_pos == 'K':
            self.__get_k()

        self.x, self.regressor = self.__train()

    def predict(self) -> [float]:
        if self.x is None and self.regressor is None:
            return "Not enough data to predict."
        return self.regressor.predict(self.x)

    def __scrape(self, option: int) -> pd.DataFrame:
        url_head = r'https://www.nfl.com/players/'
        url_feet = '/stats/career'
        url = url_head + self.player_name + url_feet
        df = pd.read_html(url)

        return df[option]  # option of 0 = first table, 1 = second table

    def __train(self) -> Union[pd.DataFrame, xgb.XGBRegressor]:
        data, label = self.seasonal_data.iloc[:, :-1], self.seasonal_data.iloc[:, -1]
        xgb.DMatrix(data=data, label=label, enable_categorical=True)

        data_train, data_test = data.iloc[1:], data.iloc[:1]  # most recent season
        label_train, label_test = label.iloc[1:], label.iloc[:1]

        if data_train is None or data_test is None:
            return None, None

        regressor = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.5, learning_rate=0.05,
                                     max_depth=5, alpha=20, n_estimators=300)
        regressor.fit(data_train, label_train)

        # print("Test: ", label_test.to_string())  # used for tweaking the model
        return data_test, regressor

    # Still need Defense

    def __get_k(self):
        # deal with the kicker stuff
        fantasy_points = []
        df = self.__scrape(0)  # get kicking

        dict = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': []}
        final_df = pd.DataFrame(dict)

        for i in range(df.shape[0] - 1):
            points = 0
            contents = []

            # calculate points gained and penalty for 0-39 yd FGs
            data = df.at[i, '30-39']
            data = data.split('-')

            temp1 = int(data[0])
            other = int(data[1])
            penalty = other - temp1

            data = df.at[i, '20-29']
            data = data.split('-')
            temp2 = int(data[0])
            other = int(data[1])
            penalty += other - temp2

            data = df.at[i, '1-19']
            data = data.split('-')
            temp3 = int(data[0])
            other = int(data[1])
            penalty += other - temp3

            points += (temp1 + temp2) * 5
            points -= penalty * 2

            contents.append(temp1 + temp2)
            contents.append(penalty)

            # calculate points gained and penalty for 40-49 yard FGs
            data = df.at[i, '40-49']
            data = data.split('-')
            temp1 = int(data[0])
            other = int(data[1])
            penalty = other - temp1

            points += temp1 * 4
            points -= penalty

            contents.append(temp1)
            contents.append(penalty)

            # calculate points gained for 50+ yard FGs
            data = df.at[i, '60+']
            data = data.split('-')
            temp1 = int(data[0])

            data = df.at[i, '50-59']
            data = data.split('-')
            temp2 = int(data[0])

            points += (temp1 + temp2) * 5

            # formulate the data so xgboost can interpret it
            contents.append(temp1 + temp2)
            contents.append(df.at[i, 'FGM'])
            contents.append(df.at[i, 'FG ATT'])
            contents.append(df.at[i, 'PCT'])
            temp = pd.DataFrame(dict)
            temp.loc[len(df.index)] = contents
            final_df = pd.concat([final_df, temp], axis=0)

            fantasy_points.append(points)

        fantasy_points.append(sum(fantasy_points))  # this line calculates the total sum of all fantasy points on table
        df['Fantasy Points'] = fantasy_points

        df.drop('YEAR', axis=1, inplace=True)
        df.drop('TEAM', axis=1, inplace=True)
        df.drop('G', axis=1, inplace=True)

        df.drop(df.shape[0] - 1, axis=0, inplace=True)

        df = df[::-1]

        temp = pd.DataFrame()
        temp['0-39-good'] = final_df['0']
        temp['0-39-miss'] = final_df['1']
        temp['40-49-good'] = final_df['2']
        temp['40-49-miss'] = final_df['3']
        temp['50+good'] = final_df['4']
        temp['FGM'] = final_df['5']
        temp['FG ATT'] = final_df['6']
        temp['PCT'] = final_df['7']
        temp['Fantasy Points'] = df['Fantasy Points']
        target = df['Fantasy Points'].tolist()
        target.pop(0)
        target.append(0)
        temp['Target'] = target
        df = temp
        df = df[::-1]  # reverse the rows

        self.seasonal_data = df.fillna(0)  # update data

    def __get_te(self):
        fantasy_points = []
        df = self.__scrape(0)  # get receiving

        for i in range(df.shape[0] - 1):
            # for te
            points = 0

            # receiving TD
            rush_td = df.at[i, 'TD']
            points += (rush_td * 6)

            # receiving YDs
            rush_yds = df.at[i, 'YDS'] * 0.1
            points += rush_yds

            fantasy_points.append(points)

        fantasy_points.append(sum(fantasy_points))  # this line calculates the total sum of all fantasy points on table
        df['Fantasy Points'] = fantasy_points

        df.drop('YEAR', axis=1, inplace=True)
        df.drop('TEAM', axis=1, inplace=True)
        df.drop('G', axis=1, inplace=True)

        df.drop(df.shape[0] - 1, axis=0, inplace=True)

        df = df[::-1]

        temp = pd.DataFrame()
        temp['re-REC'] = df['REC']
        temp['re-YDS'] = df['YDS']
        temp['re-AVG'] = df['AVG']
        temp['re-LNG'] = df['LNG']
        temp['re-TD'] = df['TD']
        temp['re-1st'] = df['1st']
        temp['re-1st'] = df['1st%']
        temp['re-20+'] = df['20+']
        temp['re-40+'] = df['40+']
        temp['Fantasy Points'] = df['Fantasy Points']
        target = df['Fantasy Points'].tolist()
        target.pop(0)
        target.append(0)
        temp['Target'] = target
        df = temp
        df = df[::-1]  # reverse the rows

        self.seasonal_data = df.fillna(0)  # update data


    def __get_rb_wr(self, flag: int):
        # This function calculates a rough estimate for players fantasy points
        fantasy_points = []

        if flag == 0:
            # for rb
            df = self.__scrape(0)  # get rushing
            df2 = self.__scrape(1)  # get receiving
        else:
            # for wr
            df = self.__scrape(1)  # get rushing
            df2 = self.__scrape(0)  # get receiving

        '''if df.shape[0] < 2:
            self.seasonal_data = None
            return'''

        for i in range(df.shape[0] - 1):
            # rushing TD
            rush_td = df.at[i, 'TD']
            points = (rush_td * 6)

            # rushing YDs
            rush_yds = df.at[i, 'YDS'] * 0.1
            points += rush_yds

            # receiving TD
            rush_td = df2.at[i, 'TD']
            points += (rush_td * 6)

            # receiving YDs
            rush_yds = df2.at[i, 'YDS'] * 0.1
            points += rush_yds

            fantasy_points.append(points)


        df, df2, fantasy_points = self.__helper(df, df2, fantasy_points)

        # copy dataframe to make the target column for the XGBoost
        temp = pd.DataFrame()


        if df.isnull().sum().sum() >= (df.shape[0]/2):
            print("Pass")
        else:
            temp['ru-ATT'] = df['ATT']
            temp['ru-YDS'] = df['YDS']
            temp['ru-AVG'] = df['AVG']
            temp['ru-LNG'] = df['LNG']
            temp['ru-TD'] = df['TD']
            temp['ru-1st'] = df['1st']
            temp['ru-1st%'] = df['1st%']
            temp['ru-20+'] = df['20+']
            temp['ru-40+'] = df['40+']
            temp['ru-FUM'] = df['FUM']

        temp['re-REC'] = df2['REC']
        temp['re-YDS'] = df2['YDS']
        temp['re-AVG'] = df2['AVG']
        temp['re-LNG'] = df2['LNG']
        temp['re-TD'] = df2['TD']
        temp['re-1st'] = df2['1st']
        temp['re-1st'] = df2['1st%']
        temp['re-20+'] = df2['20+']
        temp['re-40+'] = df2['40+']

        temp['Fantasy Points'] = df['Fantasy Points']
        target = df['Fantasy Points'].tolist()
        target.pop(0)
        target.append(0)
        temp['Target'] = target
        df = temp
        df = df[::-1]  # reverse the rows

        self.seasonal_data = df.fillna(0)  # update data

    def __get_qb(self):
        # This function calculates a rough estimate for a QBs fantasy points
        fantasy_points = []
        df = self.__scrape(0)  # get passing
        df2 = self.__scrape(1)  # get rushing

        # fantasy calculations
        for i in range(df.shape[0] - 1):
            # passing yard fantasy calculation
            yard_val = df.at[i, 'YDS'] * 0.04
            points = yard_val

            # passing touchdown fantasy calculation
            pass_val = df.at[i, 'TD']
            points += (pass_val * 4)

            # interception fantasy calculation
            points -= df.at[i, 'INT']

            # rushing TD
            rush_td = df2.at[i, 'TD']
            points += (rush_td * 6)

            # rushing YDs
            rush_yds = df2.at[i, 'YDS'] * 0.1
            points += rush_yds

            fantasy_points.append(points)

        df, df2, fantasy_points = self.__helper(df, df2, fantasy_points)

        # copy dataframe to make the target column for the XGBoost
        temp = pd.DataFrame()
        temp['p-COMP'] = df['COMP']
        temp['p-PCT'] = df['PCT']
        temp['p-YDS'] = df['YDS']
        temp['p-AVG'] = df['AVG']
        temp['p-LNG'] = df['LNG']
        temp['p-TD'] = df['TD']
        temp['p-INT'] = df['INT']
        temp['p-1st'] = df['1st']
        temp['p-1st%'] = df['1st%']
        temp['p-20+'] = df['20+']
        temp['p-SCK'] = df['SCK']
        temp['p-SCKY'] = df['SCKY']
        temp['p-RATE'] = df['RATE']

        temp['ru-ATT'] = df2['ATT']
        temp['ru-YDS'] = df2['YDS']
        temp['ru-AVG'] = df2['AVG']
        temp['ru-LNG'] = df2['LNG']
        temp['ru-TD'] = df2['TD']
        temp['ru-1st'] = df2['1st']
        temp['ru-1st%'] = df2['1st%']
        temp['ru-20+'] = df2['20+']
        temp['ru-40+'] = df2['40+']
        temp['ru-FUM'] = df2['FUM']

        temp['Fantasy Points'] = df['Fantasy Points']
        target = df['Fantasy Points'].tolist()
        target.pop(0)
        target.append(0)
        temp['Target'] = target
        df = temp
        df = df[::-1]  # reverse the rows

        self.seasonal_data = df.fillna(0)  # update data
        # self.seasonal_data.drop(0, axis=0, inplace=True)  # used for tweaking the model

    def __helper(self, df: pd.DataFrame, df2: pd.DataFrame, fantasy_points: [float]):
        fantasy_points.append(sum(fantasy_points))  # this line calculates the total sum of all fantasy points on table
        df['Fantasy Points'] = fantasy_points

        # get rid of total row and bad data
        df.drop(df.shape[0] - 1, axis=0, inplace=True)
        df2.drop(df2.shape[0] - 1, axis=0, inplace=True)

        df.drop('YEAR', axis=1, inplace=True)
        df.drop('TEAM', axis=1, inplace=True)
        df.drop('G', axis=1, inplace=True)

        df2.drop('YEAR', axis=1, inplace=True)
        df2.drop('TEAM', axis=1, inplace=True)
        df2.drop('G', axis=1, inplace=True)

        df = df[::-1]  # reverse the rows
        df2 = df2[::-1]

        return df, df2, fantasy_points


'''
# example use
fb = FantasyBoost(player_name='jahan-dotson', player_pos='WR')
pred = fb.predict()
print("Jahan Dotson: ", pred)


fb.change(player_name='tom-brady', player_pos='QB')
pred = fb.predict()
print("Tom Brady: ", pred)

fb.change(player_name='derrick-henry', player_pos='RB')
pred = fb.predict()
print("Derrick Henry: ", pred)

fb.change(player_name='tyreek-hill', player_pos='WR')
pred = fb.predict()
print("Tyreek Hill: ", pred)

fb.change(player_name='george-kittle', player_pos='TE')
pred = fb.predict()
print("George Kittle: ", pred)
'''