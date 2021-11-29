#include <thread>
#include <iostream>
#include <vector>
#include <chrono>
#include <string>

class Resource {
private:
    int data;
    std::string name;
public:
    Resource(std::string n) {
        name = n;
    }

    int getData() {
        return data;
    }

    std::string getName() {
        return name;
    }

    void setData(int x) {
        data = x;
    }

    bool operator==(Resource const &obj) {
        return this == &obj;
    }
};

class SimpleLockManager {
private:
    std::thread* th;
    std::vector<Resource*> locked_res;

public:
    SimpleLockManager() {
    }

    void lock(Resource& target) {
        // Wait until lock not in table
        // Using logical and short-circuit
        for (unsigned i = 0; i < locked_res.size(); ++i)
            while (i < locked_res.size() && (*locked_res[i]) == target)
                std::this_thread::sleep_for(std::chrono::milliseconds(100));

        locked_res.push_back(&target);
    }

    void unlock(Resource& target) {
        for (auto itr = locked_res.begin(); itr != locked_res.end(); ++itr) {
            if (**itr == target) {
                locked_res.erase(itr);
                break;
            }
        }
    }
};


class Transaction {
private:
    SimpleLockManager &lock_manager_ref;
    std::string transaction_name;
    std::vector<Resource*> locked_res;
public:
    Transaction(std::string n, SimpleLockManager &lm) : lock_manager_ref(lm) {
        transaction_name = n;
        std::cout << "Transaction " << transaction_name << " started\n";
    }

    void write(Resource &res, int value) {
        std::cout << "W" << transaction_name << "(" << res.getName() << ")\n";
        res.setData(value);
    }

    int read(Resource &res) {
        std::cout << "R" << transaction_name << "(" << res.getName() << ")\n";
        return res.getData();
    }

    void exclusiveLock(Resource &res) {
        lock_manager_ref.lock(res);
        locked_res.push_back(&res);
        std::cout << "XL" << transaction_name << "(" << res.getName() << ") acquired\n";
    }

    void unlock(Resource &res) {
        lock_manager_ref.unlock(res);
        std::cout << "U" << transaction_name << "(" << res.getName() << ") released\n";
    }

    void commit() {
        for (auto itr = locked_res.begin(); itr != locked_res.end(); ++itr)
            lock_manager_ref.unlock(**itr);
        std::cout << "Transaction " << transaction_name << " committed\n";
    }
};





SimpleLockManager manager;
Resource a = Resource("A");
Resource b = Resource("B");

void transaction1() {
    Transaction t1 = Transaction("1", manager);
    t1.exclusiveLock(a);
    t1.write(a, 10000);
    t1.unlock(a);

    t1.exclusiveLock(b);
    t1.write(b, t1.read(b) + 800000);
    t1.commit();
}

void transaction2() {
    Transaction t2 = Transaction("2", manager);
    t2.exclusiveLock(a);
    t2.exclusiveLock(b);
    t2.write(a, t2.read(a) + 40);
    t2.write(b, 900);
    t2.commit();
}

int main() {
    a.setData(10);
    b.setData(40);
    std::thread thtr1 = std::thread(transaction1);
    std::thread thtr2 = std::thread(transaction2);
    thtr1.join();
    thtr2.join();

    std::cout << "\nResult\n";
    std::cout << a.getData() << "\n";
    std::cout << b.getData() << "\n";
    return 0;
}
