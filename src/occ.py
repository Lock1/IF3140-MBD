class ReadTransaction:
    def __init__(self, number):
        self.number = number
        self.data = dict()

    def readTransaction(self, item, timestamp):
        if item in self.data.values():
            idx = list(self.data.values()).index(item)
            oldTimestamp = list(self.data.keys())[idx]
            self.data[timestamp] = self.data.pop(oldTimestamp)
        else:
            self.data[timestamp] = item

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

class Schedule:
    def __init__(self):
        self.data = dict()
        
    def write(self, item, number):
        if number not in self.data:
            self.data[item] = []

        self.data[item].append(number)

class CachedSchedule:
    def __init__(self):
        self.db = Schedule()
        self.transactions = dict()
        self.writeData = dict()

    def read(self, item, number, timestamp):
        idx = number 
        if idx not in self.transactions:
            self.transactions[idx] = ReadTransaction(number)
        self.transactions[idx].readTransaction(item, timestamp)

        print(f'[R] Read-{item} on Transaction {number}')

    def write(self, item, number, timestamp):
        if self.isConflict(item, number):
            print(f'[W] Rollback on Write-{item} on Transaction {number}...')
        self.writeData[timestamp] = item
        self.db.write(item, number)
        print(f'[W] Write-{item} on Transaction {number}')

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
        if (trans.lower() != 'c'):
            number = trans[1]
            type = trans[0]
            item = trans[3]
            if (type.lower() == 'r'):
                cs.read(item, int(number), i)
            elif (type.lower() == 'w'):
                cs.write(item, int(number), i)
        i += 1
    print('Committed')

if __name__ == '__main__':
    main()