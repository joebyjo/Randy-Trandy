import json
from datetime import datetime
from random import choice


class TimeTable:
    sunday = ['Hindi/French', 'Maths', 'Economics', 'Break', 'Physics', 'Stretch', 'Biology', 'History', 'English']
    monday = ['English', 'Maths', 'Hindi/French', 'Break', 'Geography', 'Stretch', 'IT', 'NAP-eng', 'NAP-math']
    tuesday = ['Test', 'Test', 'Break', 'Maths', 'Chemistry', 'English', 'Break', 'Civics', 'NAP-science']
    wednesday = ['Hindi/French', 'English', 'Biology', 'Break', 'Maths', 'Stretch', 'Civics', 'Maths', 'IT']
    thursday = ['Geography', 'Hindi/French', 'Physics', 'Break', 'ME', 'Stretch', 'English', 'Maths', 'Chemistry']

    week = [sunday, monday, tuesday, wednesday, thursday]

    def get_day(self, days=None):
        if days is None:
            days = int(datetime.now().strftime('%w'))
        day = TimeTable.week[days]
        return day

    def get_time(self, time=None):
        if time is None:
            time = int(datetime.now().strftime('%H%M'))
        return time

    def get_period(self, _day=None, _time=None):

        day = self.get_day(_day)
        time = self.get_time(_time)

        if int(datetime.now().strftime('%w')) != 2:
            if 800 <= time < 845:
                return day[0]
            elif 846 <= time < 930:
                return day[1]
            elif 931 <= time < 1015:
                return day[2]
            elif 1016 <= time < 1030:
                return day[3]
            elif 1031 <= time < 1115:
                return day[4]
            elif 1116 <= time < 1130:
                return day[5]
            elif 1131 <= time < 1215:
                return day[6]
            elif 1216 <= time < 1300:
                return day[7]
            elif 1301 <= time < 1345:
                return day[8]
            else:
                return f'No school at {datetime.now().strftime("%I:%M %p")}'

        elif day == 2:
            if 755 <= time < 840:
                return day[0]
            elif 841 <= time < 935:
                return day[1]
            elif 936 <= time < 945:
                return day[2]
            elif 946 <= time < 1030:
                return day[3]
            elif 1031 <= time < 1115:
                return day[4]
            elif 1116 <= time < 1200:
                return day[5]
            elif 1131 <= time < 1215:
                return day[6]
            elif 1216 <= time < 1300:
                return day[7]
            elif 1301 <= time < 1345:
                return day[8]
            else:
                return f'No school at {datetime.now().strftime("%I:%M %p")}'

    def get_next_period(self, x=None, y=None):

        day = self.get_day(x)
        time = self.get_time(y)

        if day != 2:
            if 800 <= time < 845:
                return day[1]
            elif 846 <= time < 930:
                return day[2]
            elif 931 <= time < 1015:
                return day[3]
            elif 1016 <= time < 1030:
                return day[4]
            elif 1031 <= time < 1115:
                return day[5]
            elif 1116 <= time < 1130:
                return day[6]
            elif 1131 <= time < 1215:
                return day[7]
            elif 1216 <= time < 1300:
                return day[8]
            elif 1301 <= time < 1345:
                return 'This is the last period'
            else:
                return 'School is over!'

        elif day == 2:
            if 755 <= time < 840:
                return day[1]
            elif 841 <= time < 935:
                return day[2]
            elif 936 <= time < 945:
                return day[3]
            elif 946 <= time < 1030:
                return day[4]
            elif 1031 <= time < 1115:
                return day[5]
            elif 1116 <= time < 1200:
                return day[6]
            elif 1131 <= time < 1215:
                return day[7]
            elif 1216 <= time < 1300:
                return day[8]
            elif 1301 <= time < 1345:
                return 'This is the last period'
            else:
                return 'School is over!'



