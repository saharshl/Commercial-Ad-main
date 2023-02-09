# Commercial-Ad Detection MVP 
***
## Contents
Main

* final_mac_test.py - File that contains the source code which runs the software behind detecting ads 
* nowtv_best.pt - File that stores the detection model information for "Now TV". Needs to be called by the detection file

Tests

* This folder contains all the extra files that were used to test logic and blocks of code
* You can add new test files to this folder as per new test cases

***

## How To Use

### Step 0: Installations (Using Terminal)


#### Homebrew

* **(For Mac)** Install Homebrew by following instructions [here](https://brew.sh/)

* **(For Windows)** Install equivalent of Homebrew

#### PyEnv and Python

* Follow the steps in the Youtube link [here](https://www.youtube.com/watch?v=-5vd5GEpF-w)

#### VS Code

* Install VS Code on the desired OS

* Open VS Code

* Go To Extensions -> Python -> Install

#### OpenCV

```
brew install opencv
```

#### OpenCV Python

```
pip install opencv-python
```

```
pip install opencv-contrib-python
```

#### PyTorch

* Install required PyTorch version [here](https://pytorch.org/)

#### Selenium

```
pip install selenium
```

#### Pandas

```
pip install pandas
```

#### TQDM

```
pip install tqdm
```

#### Matplotlib

```
pip install matplotlib
```

#### Seaborn

```
pip install seaborn
```

#### NumPy

```
pip install numpy
```

***

### Step 1: Open File

* Start with downloading "**final_mac_test.py**" and "**nowtv_best.pt**" in local folder.

* Next, add the folder to VS code

* Open the "**final_mac_test.py**" file in VS Code

### Step 2: Add desired wesbite link to File

* You have to add the website link that plays the content, to the file

```
tv_link = 'https://news.now.com/home/live'
```

* Replace the value in the 'tv_link' variable with the desired website (In this case, its NowTV)

### Step 3: Extract "m3u8" URL from website and add to file

* Has been automated

### Step 4: Add detection model "nowtv_best.pt" to File path

* In order for detection to work, need to add the detection model thus downloaded to the file in the 'detection' variable

* In the detection variable, add the detection model by naming the path to it

* To know more about paths, click [here](https://docs.oracle.com/javase/tutorial/essential/io/path.html)

```
detection = ObjectDetection('/Users/saharsh/Desktop/Ad_Detect/NowTV/nowtv_best.pt',tv_link)
```

### Step 5: Save and Run

* Finally, save the file

* Then, run the file from the Terminal and watch it execute the detection

***

## Points To Note

* Currently, I have used a dummy YT link to switch to when the algorithm detects an add on the TV program

  - You can change the link to any desired link as per your convenience
  ```
  self.driver.get('https://www.youtube.com/watch?v=wmw6YyMie30')
  ```
  - You can change the YT link by editing the above line
  
* The program needs to be manually fed in the "m3u8" url by extracting from the website

  - The m3u8 url from the website typically expires in 25-30 mins
  - Hence, it is important to update that link every 25-30 mins to ensure detection continues without erros
  - If working with NowTV, make sure to get the URL which contains "Stream(02)"
  
* Currently, the detection only supports "m3u8" format. 
 
* Currently, the detection model is only made for NowTV. New TV channels will require new detection models (Or one composite detection model)

* Currently, the automation of extraction of the tv streaming link from the wesbite works only for NowTV. The code has comment snippets with specific instruction to adjust extraction based on desired website.

***

## Ongoing Work

* Research into decoding information from "mpd" URL for new content
