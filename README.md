### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [Project structure & file description](#files)
4. [Results](#results)

## Installation <a name="installation"></a>

There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python.  The code should run with no issues using Python versions 3.*.

## Project Motivation<a name="motivation"></a>

For this project, I was interested in using Stack Overflow data from 2017 to better understand:

Since we had the opportunity to have access to AirBnb data, I thought it would be interesting to dig into what makes a listing successful or not
in the platform:

1. Starting with looking at how the market looks like in Boston's districts? (e.g. overall demand and occupation rate per location)
2. Digging into understanding how the price of a listing can be determined considering various characteristics of a listing
3. Finally, we'll see if we can actually predict the success of a listing aka it's occupation rate at 60d.

## Project structure & file description <a name="files"></a>

```
nd-blogpost
├── data
│   │── airbnb_listings_boston
│── exploration
│   │── EDA-listings_airbnb.ipynb
├── requirements.txt
├── readme.md
```

Project is made of 2 main folders:
`data` contains the datasets used during the preparation and analysis work. Analysis is using airbnb data only.
`exploration` contains one notebook where the 3 questions are being addressed.
`requirements.txt` contains the packages to be installed to run the notebook.
`readme.md` describes the structure of the project.


## Results<a name="results"></a>

The main findings of the code can be found at the post available [here](https://medium.com/@josh_2774/how-do-you-become-a-developer-5ef1c1c68711).
