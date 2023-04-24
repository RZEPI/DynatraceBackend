# Dynatrace recruitment task - back-end/fullstack 

## How to run the program?
To clone the repository, in your console input this commands
```
git init
git clone https://github.com/RZEPI/DynatraceBackend/
```
The program can be easly run on both Linux and Windows. The project contains 2 initalization files: initialization.sh - for Linux and initialization.bat - for Windows.

For Linux: 
```
chmod +x initialization.sh
./initialization.sh
```
For Windows:
```
./initialization.bat
```
Nextly, in your browser type `localhost:8888` in search bar to use GUI  
Usage of command `curl` in command prompt is also handled but unrecommanded(it returns whole header on Windows)  
Example of text command:
```
curl http://localhost:8888/minmaxval/gbp/2
```

### How to run tests?
To run tests make sure that you are in virtual environment which was made executing one of scripts  
For Linux:
```
source venv/bin/activate
```
For Windows:
```
.\venv\Scripts\activate
```
than run a following command
``` 
python tests.py 
```
