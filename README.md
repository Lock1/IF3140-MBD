# Concurrency Control Protocol

## Simple Locking Implementation
Untuk menjalankan program simple_lock.cpp diperlukan :
- Compiler g++ dan library thread
```sh
g++ -pthread -o out simple_lock.cpp
```
- Command untuk run program:
```sh
./[hasil compile]
```

## OCC Implementation
Untuk menjalankan program occ.py diperlukan:
- python3
- Command untuk run program:
```sh
python3 occ.py
```

Untuk contoh inputnya formatnya adalah sebagai berikut:
<br>
```R1(X); W2(X); W2(Y); W3(Y); W1(Y); C1; C2; C3;```

## MVCC Implementation
Untuk menjalan program mvcc.py diperlukan :
- python3
- Command untuk run program:
```sh
python3 mvcc.py
```

Config pada mvcc.py sudah dijelaskan pada program, jika ingin mengedit config ikuti arahan komentar pada program
