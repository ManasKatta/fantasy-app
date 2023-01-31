import pandas as pd
import xgboost as xgb
from typing import Union


class FantasyBoost:

    def __init__(self, player_name: str, player_pos: str):
        self.player_name, self.seasonal_data, self.x, self.regressor = None, None, None, None
        self.change(player_name, player_pos)

    def change(self, player_name: str, player_pos: str):
        self.player_name = player_name

        if player_pos == 'QB':
            self.__get_qb()  # self.seasonal_data gets updated within this function
            # self.seasonal_data.to_csv('jalen_hurts.csv')
        elif player_pos == 'RB':
            self.__get_rb()
        elif player_pos == 'WR':
            self.__get_wr()
        elif player_pos == 'TE':
            self.__get_te()

        self.x, self.regressor = self.__train()

    def predict(self) -> [float]:
        return self.regressor.predict(self.x)

    def __scrape(self, option: int) -> pd.DataFrame:
        url_head = 'https://www.nfl.com/players/'
        url_feet = '/stats/career'
        url = url_head + self.player_name + url_feet
        df = pd.read_html(url)

        return df[option]  # option of 0 = first table, 1 = second table

    def __train(self) -> Union[pd.DataFrame, xgb.XGBRegressor]:
        data, label = self.seasonal_data.iloc[:, :-1], self.seasonal_data.iloc[:, -1]
        xgb.DMatrix(data=data, label=label)

        data_train, data_test = data.iloc[1:], data.iloc[:1]  # most recent season
        label_train, label_test = label.iloc[1:], label.iloc[:1]
        regressor = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.5, learning_rate=0.05,
                                     max_depth=5, alpha=20, n_estimators=300)
        regressor.fit(data_train, label_train)

        # print("Test: ", label_test.to_string())  # used for tweaking the model
        return data_test, regressor

    # Still need RBs, WRs, TEs, K, Defense

    def __get_te(self):
        pass

    def __get_wr(self):
        pass

    def __get_rb(self):
        pass

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


# example use
fb = FantasyBoost(player_name='jalen-hurts', player_pos='QB')
pred = fb.predict()
print(pred)

fb.change(player_name='patrick-mahomes', player_pos='QB')
pred = fb.predict()
print(pred)
