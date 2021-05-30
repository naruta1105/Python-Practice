class FileSave():
    def __init__(self,fileName):
        self.fileName = fileName
        self.highestScore = 0
        if path.exists(self.fileName) :
            with open(self.fileName,'r') as f:
                try :
                    df = pd.read_csv(f, usecols= ['Score'])
                    lst = df.values.tolist()
                    self.highestScore = max(lst)[0]
                except:
                    print("No column")
                f.close()

    def saveFileData(self,score):
        #df = pd.DataFrame([[list_direction,list_food,score]], columns = ['Direction', 'Food Position', 'Score'])
        df = pd.DataFrame([[score]], columns = ['Score'])
        if not path.exists(self.fileName) :
            with open(self.fileName,'w', newline='') as f:
                df.to_csv(f, index=False, encoding='utf-8',header=True)
                f.close()
        else:
            with open(self.fileName, 'a+', newline='') as f:
                df.to_csv(f, index=False, encoding='utf-8', mode='a',header=False)
                f.close()