#include <thread>
#include <iostream>
#include <vector>
#include <chrono>

class Resource {
private:
    int data;
public:
    Resource() {

    }

    int getData() {
        return data;
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

    ~SimpleLockManager() {
    }

    void lock(Resource& target) {
        // Wait until lock not in table
        // Using logical and short-circuit
        for (unsigned i = 0; i < locked_res.size(); ++i)
            while (i < locked_res.size() && (*locked_res[i]) == target)
                std::this_thread::sleep_for(std::chrono::milliseconds(50));

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





Resource a, b;
SimpleLockManager manager;
void transaction1() {
    manager.lock(a);
    std::cout << "XL1(A) acquired\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    std::cout << "W(A) 10000\n";
    a.setData(10000);
    manager.unlock(a);
    std::cout << "XL1(A) released\n";

    manager.lock(b);
    std::cout << "XL1(B) acquired\n";
    std::cout << "W(B) " << b.getData() << " + 800000\n";
    b.setData(b.getData() + 800000);
    manager.unlock(b);
    std::cout << "XL1(B) released\n";
}

void transaction2() {
    manager.lock(a);
    manager.lock(b);
    std::cout << "XL2(A) acquired\n";
    std::cout << "XL2(B) acquired\n";
    std::cout << "W(A) " << a.getData() << " + 800000\n";
    a.setData(a.getData() + 40);
    std::cout << "W(B) 900\n";
    b.setData(900);
    manager.unlock(b);
    manager.unlock(a);
    std::cout << "XL2(A) released\n";
    std::cout << "XL2(B) released\n";
}

int main() {
    a.setData(10);
    b.setData(40);
    std::thread thtr1 = std::thread(transaction1);
    std::thread thtr2 = std::thread(transaction2);
    thtr1.join();
    thtr2.join();

    std::cout << "Result\n";
    std::cout << a.getData() << "\n";
    std::cout << b.getData() << "\n";
    return 0;
}
