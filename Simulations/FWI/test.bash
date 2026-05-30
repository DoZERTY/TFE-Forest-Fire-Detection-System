# 1. Compile the source code
gcc -shared -o pyFWI-1.0/pyFWI/example.so -fPIC ./FWI_c/FWI.c

# 2. Run the test
cd pyFWI-1.0/pyFWI
python2 TestC.py

# 3. Plot the results
python3 plot.py

# 4. Clean up temporary files
rm error.txt
rm example.so
rm *.pyc