# Dynatrace recruitment task - back-end/fullstack 

## How to run the program?
To clone the repository, in your console input these commands
```
git init
git clone https://github.com/RZEPI/DynatraceBackend/
```
Than go to directory with the project
```
cd DynataceBackend
```
The program can be easily run on both Linux and Windows. The project contains 2 initalization files: initialization.sh - for Linux and initialization.bat - for Windows.   
> Remember to have admin privileges to run this commads.  

For Linux: 
```
chmod +x initialization.sh
./initialization.sh
```
For Windows:
```
initialization.bat
```
Nextly, in your browser type `localhost:8888` in search bar to use GUI  
Usage of command `curl` in command prompt is also handled but unrecommended(GUI is more user friendly)  
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
venv\Scripts\activate
```
than run a following command
``` 
python tests.py 
```

## Examples of text commands

To get response with result of queries we are using ``curl`` command in pattern  

```
curl http://localhost:8888/<name_of_query>/<data1>/<data2>
```
1. to get an average exchange rate of a given currency(data1), at a given date(data2)  
Example:
```
curl http://localhost:8888/exchanges/GBP/2023-01-02
```
2. to get max and min average value of a given currency(data1) for number of last quotations(data2)  
Example:
```
curl http://localhost:8888/minmaxval/GBP/10
```
3. to get a major difference between the buy and ask rate of a given currency(data1) for number of last quotations(data2)  
Example:
```
curl http://localhost:8888/majordiff/GBP/10
```
