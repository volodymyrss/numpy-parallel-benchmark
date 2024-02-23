#include <iostream>
#include <chrono>
using namespace std;

int main(int argc, char* argv[]) {
    
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <number>" << std::endl;
        return 1;
    }

    long int memory_scale_m = std::stol(argv[1]);
    int duration = std::stoi(argv[2]);


    int i=0;
    int j=0;
    long int length = memory_scale_m * 1000 * 1000;
        
  
    double* array{ new double[length]{} };

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    
    for (i=0;i<length;i++) {
        array[i]=i;
    }


    for (j=0;j<duration;j++) {
    for (i=0;i<length;i++) {
        array[i]=array[i]*2;
    }}

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << "[ms]" << std::endl;

  return 0;
}
