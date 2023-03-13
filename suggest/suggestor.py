# This program is the suggestion algorithm. It takes in information about the fantasy league and projected points for each player.
# It outputs an array of trades and the value of each trade.

import pandas as pd
PRINT_DEBUG = False

def printd(string):
    if PRINT_DEBUG:
        print(str(string))

    return

class Player():
    def __init__(self, sleeper_id, position, points):
        self.id = sleeper_id
        self.proj = points
        self.pos = position
        self.paa = 0
        self.par = 0
        return

    def get_paa(self, avg):
        self.paa = self.proj - avg
        printd(f"paa: {self.paa}")
        return

    def get_par(self, repl):
        self.par = self.proj - repl
        return

    def print_player(self):
        printd(f"ID = {self.id}, Position = {self.pos}, Points = {self.proj}, PAA = {self.paa}, PAR = {self.par}")
        return

class Trade():
    def __init__(self, give, receive):
        self.g1 = give
        self.r1 = receive
        self.generate_value()

    def print_trade(self):
        if len(self.g1)==1 and len(self.r1)==1:
            print(f"Give {self.g1[0].id} for {self.r1[0].id}, value: {self.val}")
        elif len(self.g1)==1 and len(self.r1)==2:
            print(f"Give {self.g1[0].id} for {self.r1[0].id} and {self.r1[1].id}, value: {self.val}")
        elif len(self.g1)==2 and len(self.r1)==1:
            print(f"Give {self.g1[0].id} and {self.g1[1].id} for {self.r1[0].id}, value: {self.val}")
        else:
            print(f"Give {self.g1[0].id} and {self.g1[1].id} for {self.r1[0].id} and {self.r1[1].id}, value: {self.val}")

    def get_given(self):
        return self.g1

    def get_received(self):
        return self.r1
    
    def generate_value(self):
        value=0
        for p1 in self.g1:
            value-=p1.par
        for p2 in self.r1:
            value+=p2.par
        self.val = value

    def get_value(self):
        return self.val

class Suggestor():

    def __init__(self, playerfiles, leaguefile):
        self.league_size = 0
        self.rb_num = 0
        self.wr_num = 0
        self.te_num = 0
        self.qb_num = 0

        self.player_list = []
    
        for pf in playerfiles:
            self.read_player_info(pf)

        self.read_league_info(leaguefile)

        self.make_arrays()
        self.sort_pts()

        self.get_players_paa()
        self.get_players_par()

        self.print_lists()
        return

    def get_player(self, id):
        for p in self.player_list:
            if p.id==id:
                return p

    def read_player_info(self, playerfile):                                     # Reads from the player data input file
        
        pfile = pd.read_csv(playerfile)

        printd(str(pfile))
        for i in range(0,pfile.shape[0]):
            printd(i)
            id = pfile.ID[i]
            pos = pfile.Position[i]
            pts = pfile.Points[i]
            p = Player(id, pos, pts)
            p.print_player()
            self.player_list.append(p)
        return

    def read_league_info(self, leaguefile):                                     # Reads from the league info file
        self.league_size = 2
        self.league_ppr = 0
        self.rb_num = 2
        self.wr_num = 2
        self.qb_num = 1
        self.te_num = 1

        rosters = [['josh-allen-4','jonathan-taylor','derrick-henry','justin-jefferson','cooper-kupp','mark-andrews'],['patrick-mahomes','dalvin-cook','austin-ekeler','tyreek-hill','jaylen-waddle','travis-kelce']]
        self.roster_list = []

        for r in rosters:
            r1 = []
            for p in r:
                p1 = self.get_player(p)
                r1.append(p1)
            self.roster_list.append(r1)

        p1roster = ['josh-allen-4','jonathan-taylor','derrick-henry','justin-jefferson','cooper-kupp','mark-andrews']
        self.p1_roster = []

        for p in p1roster:
            p1 = self.get_player(p)
            self.p1_roster.append(p1)

        printd(f'RB num: {self.rb_num}')
        return

    def make_arrays(self):
        self.rb_list = []
        self.wr_list = []
        self.te_list = []
        self.qb_list = []
        for p1 in self.player_list:
            if p1.pos == 'rb':
                self.rb_list.append(p1)
            if p1.pos == 'wr':
                self.wr_list.append(p1)
            if p1.pos == 'te':
                self.te_list.append(p1)
            if p1.pos == 'qb':
                self.qb_list.append(p1)

    def sort_pts(self):
        self.wr_list = sorted(self.wr_list, key=lambda x: x.proj, reverse=True)
        self.rb_list = sorted(self.rb_list, key=lambda y: y.proj, reverse=True)
        self.te_list = sorted(self.te_list, key=lambda x: x.proj, reverse=True)
        self.qb_list = sorted(self.qb_list, key=lambda y: y.proj, reverse=True)

    def sort_paa(self):
        self.rb_paa = sorted(self.rb_list, key=lambda x: x.paa, reverse=True)
        self.wr_paa = sorted(self.wr_list, key=lambda y: y.paa, reverse=True)
        self.te_paa = sorted(self.te_list, key=lambda x: x.paa, reverse=True)
        self.qb_paa = sorted(self.qb_list, key=lambda y: y.paa, reverse=True)

    def sort_par(self):
        self.rb_par = sorted(self.rb_list, key=lambda x: x.par, reverse=True)
        self.wr_par = sorted(self.wr_list, key=lambda y: y.par, reverse=True)
        self.te_par = sorted(self.te_list, key=lambda x: x.par, reverse=True)
        self.qb_par = sorted(self.qb_list, key=lambda y: y.par, reverse=True)

    def get_num(self, pos):
        if pos=='rb':
            return self.rb_num
        if pos=='wr':
            return self.wr_num
        if pos=='te':
            return self.te_num
        if pos=='qb':
            return self.qb_num

    def get_pos_average(self, pos, player_array):                                      # Returns the average score of starters for the given position
        num_start = self.league_size * self.get_num(pos)
        printd(f'{self.get_num(pos)}')
        total = 0

        for i in range(0,num_start):
            total+=player_array[i].proj

        printd(f'Total: {total}, num_start: {num_start}')
        return (total/num_start)

    def get_pos_repl(self, pos, player_array):
        num_start = self.league_size * self.get_num(pos)
        return player_array[num_start].proj

    def get_players_paa(self):                                      # Gets the points above average for all players and stores them in a list
        self.rb_avg = self.get_pos_average("rb", self.rb_list)
        self.wr_avg = self.get_pos_average("wr", self.wr_list)
        self.te_avg = self.get_pos_average("te", self.te_list)
        self.qb_avg = self.get_pos_average("qb", self.qb_list)
        for p1 in self.player_list:
            printd("here")
            if p1.pos == 'wr':
                p1.get_paa(self.wr_avg)
            if p1.pos == 'rb':
                p1.get_paa(self.rb_avg)
            if p1.pos == 'te':
                p1.get_paa(self.te_avg)
            if p1.pos == 'qb':
                p1.get_paa(self.qb_avg)
        return

    def get_players_par(self):
        self.rb_repl = self.get_pos_repl('rb', self.rb_list)
        self.wr_repl = self.get_pos_repl('wr', self.wr_list)
        self.te_repl = self.get_pos_repl('te', self.te_list)
        self.qb_repl = self.get_pos_repl('qb', self.qb_list)

        for p1 in self.player_list:
            if p1.pos == 'wr':
                p1.get_par(self.wr_repl)
            if p1.pos == 'rb':
                p1.get_par(self.rb_repl)
            if p1.pos == 'te':
                p1.get_par(self.te_repl)
            if p1.pos == 'qb':
                p1.get_par(self.qb_repl)
        return

    def print_lists(self):
        printd("Player List: ")
        for i in self.player_list:
            i.print_player()

        printd(f"RB Avg = {self.rb_avg}    WR Avg = {self.wr_avg}    TE Avg = {self.te_avg}    QB Avg = {self.qb_avg}")
        printd(f"RB Repl = {self.rb_repl}    WR Repl = {self.wr_repl}    TE Repl = {self.te_repl}    QB Repl = {self.qb_repl}")

    def get_11(self, roster):
        for p1 in self.p1_roster:
            printd('here')
            for p2 in roster:
                printd('now here')
                t1 = Trade([p1],[p2])
                printd("trade generated")
                #t1.print_trade()
                if t1.get_value() > self.trade_value_min and t1.get_value() < self.trade_value_max:
                    printd("trade within bounds")
                    self.trade_list.append(t1)
                else:
                    del t1

    def get_12(self,roster):
        num = 1
        for p1 in self.p1_roster:
            for p2 in self.p1_roster[num:]:
                for p3 in roster:
                    t1 = Trade([p1,p2],[p3])
                    #t1.print_trade()
                    if t1.get_value() > self.trade_value_min and t1.get_value() < self.trade_value_max:
                        self.trade_list.append(t1)
                    else:
                        del t1
            num+=1
        return

    def get_21(self,roster):
        for p1 in self.p1_roster:
            num = 1
            for p2 in roster:
                for p3 in roster[num:]:
                    t1 = Trade([p1],[p2,p3])
                    #t1.print_trade()
                    if t1.get_value() > self.trade_value_min and t1.get_value() < self.trade_value_max:
                        self.trade_list.append(t1)
                    else:
                        del t1

                num+=1
        return

    def get_22(self,roster):
        return

    def get_trades(self, roster):
        self.get_11(roster)
        self.get_12(roster)
        self.get_21(roster)
        self.get_22(roster)

    def generate_trades(self, value_min, value_max):
        self.trade_value_min = value_min
        self.trade_value_max = value_max
        self.trade_list = []
        printd(str(self.roster_list))
        for roster in self.roster_list:
            printd(str(roster))
            if roster==self.p1_roster:
                continue
            else:
                printd("getting trades")
                self.get_trades(roster)

    def print_trades(self):
        printd("printing trades")
        for trade in self.trade_list:
            trade.print_trade()


def main():
    leaguefile = "league.txt"
    playerfiles = ['qb_preds_seasonal.csv','wr_preds_seasonal.csv','te_preds_seasonal.csv','rb_preds_seasonal.csv']
    sug = Suggestor(playerfiles,leaguefile)
    sug.generate_trades(-50,50)
    sug.print_trades()

main()