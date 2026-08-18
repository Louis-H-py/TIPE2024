g++ -c -fPIC OthelloEngine.cpp -o OthelloEngine.o
g++ -shared -o OthelloEngine.so OthelloEngine.o