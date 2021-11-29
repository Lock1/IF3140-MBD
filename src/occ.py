class Transaction:
    def __init__(self, number):
        self.number = number
        self.readData = dict()
        self.writeData = dict()

    def readTransaction(self, item, timestamp):
        if item in self.readData.values():
            idx = list(self.readData.values()).index(item)
            oldTimestamp = list(self.readData.keys())[idx]
            self.readData[timestamp] = self.readData.pop(oldTimestamp)
        else:
            self.readData[timestamp] = item

    def writeTransaction(self, item, timestamp):
        if item in self.writeData.values():
            idx = list(self.writeData.values()).index(item)
            oldTimestamp = list(self.writeData.keys())[idx]
            self.writeData[timestamp] = self.writeData.pop(oldTimestamp)
        else:
            self.writeData[timestamp] = item

    def hasItem(self, item):
        if item in self.data.values():
            return True
        return False

    def itemTimestamp(self, item):
        if self.hasItem(item):
            idx = list(self.data.values()).index(item)
            timestamp = list(self.data.keys())[idx]
            return timestamp
        return -1

    def isRead(self, item):
        return item in self.readData.values()

class Schedule:
    def __init__(self):
        self.committed = []
        
    def commit(self, number):
        self.committed.append(number)

class CachedSchedule:
    def __init__(self):
        self.db = Schedule()
        self.transactions = dict()
        self.writeData = dict()
        self.validation = dict()

    def read(self, item, number, timestamp):
        idx = number 
        if idx not in self.transactions:
            self.transactions[idx] = Transaction(number)
        self.transactions[idx].readTransaction(item, timestamp)

    def write(self, item, number, timestamp):
        if number in self.db.committed:
            self.validation[number] = 0
        
        try:
            if not self.transactions[number].isRead(item):
                return
        except Exception:
            pass
        
        idx = number
        if idx not in self.writeData:
            self.writeData[idx] = Transaction(number)
        self.writeData[idx].writeTransaction(item, timestamp)

    def validate(self, number):
        try:
            if self.validation[number] == 0:
                return
        except Exception:
            pass

        try:
            for item in self.writeData[number].writeData.values():
                if self.isConflict(item, number):
                    self.validation[number] = 0
                else:
                    self.validation[number] = 1
        except Exception:
            self.validation[number] = 1
        
        self.db.commit(number)
        if self.validation[number] == 0:
            print(f'[C-{number}] Failed when trying to validate, commencing rollback...')
        else:
            print(f'[C-{number}] Validated')

    def getWriteTimestamp(self, item):
        if item in self.writeData.values():
            return list(self.writeData.keys())[list(self.writeData.values()).index(item)]
        return -1

    def isConflict(self, item, number):
        writeTimestamp = self.getWriteTimestamp(item)
        if writeTimestamp == -1:
            return False

        try:
            readTimestamp = self.transactions[number].itemTimestamp(item)
            if readTimestamp == -1:
                return False

            if readTimestamp > writeTimestamp:
                return False

            return True
        except Exception:
            return False

def main():
    transactions = input('Transactions: ')
    splitTransactions = [x.strip() for x in (transactions.split(';'))][:-1]
    cs = CachedSchedule()

    i = 1
    for trans in splitTransactions:
        type = trans[0]
        number = trans[1]
        if (type.lower() != 'c'):
            item = trans[3]
            if (type.lower() == 'r'):
                print(f'[R] Read-{item} on Transaction {number}')
                cs.read(item, int(number), i)
            elif (type.lower() == 'w'):
                print(f'[W] Write-{item} on Transaction {number}')
                cs.write(item, int(number), i)
        else:
            print(f'[C] Commit Transaction {number}')
            cs.validate(int(number))

        i += 1

if __name__ == '__main__':
    main()