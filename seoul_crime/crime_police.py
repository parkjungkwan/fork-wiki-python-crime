from seoul_crime.data_reader import DataReader
class CrimeModel:
    def __init__(self):
        self.dr = DataReader()

    def hook_process(self):
        print('----------- 1. CCTV 파일로 DF 생성  --------------')
        self.get_crime()

    def get_crime(self):
        self.dr.context = './data/'
        self.dr.fname = 'crime_in_seoul.csv' # 메모장 UTF-8 저장 필요
        crime = self.dr.csv_to_dframe()
        print(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울'+str(name[:-1]+'경찰서'))
        station_addrs = []
        station_lats = [] # 위도
        station_lngs = [] # 경도
        gmaps = self.dr.create_gmaps()