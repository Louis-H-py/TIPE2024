g++ -c -fPIC accelerator.cpp -o accelerator.o
g++ -shared -o accelerator.so accelerator.o