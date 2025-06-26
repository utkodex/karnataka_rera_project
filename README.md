## Table of Content
1. [Prerequisites](#Prerequisites)
    1. [Create virtual Environment](#create-virtual-environment)
    2. [How to create credentials.json](#how-to-create-credentialsjson)
    3. [Download Docker Desktop](#download-docker-desktop)
2. [How to Run](#how-to-run)
3. [DEMO](#DEMO)
    * [Scraper Instructions](#scraper-instructions)

# Prerequisites

## Create virtual Environment
```python
conda create -p env python=3.10 -y
```

## How to create credentials.json
[Watch the Video to how to create credentials.json](https://youtu.be/k_PB4ORz2r0?si=aIw30wu4buzkaPB-)

## Download Docker Desktop
[Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

# How to Run

```python
streamlit run ./main.py
```

# DEMO

![UI Photo](media/ui_pic.jpeg)

### Scraper Instructions

1. **Select the City**  
   Choose a city from the dropdown menu.

2. **Scrape Button**  
   Click on the **"Scrape"** button to start the scraping process.

3. **Mode Selection**  
   - **Headless Mode**: The scraping process runs in the background without displaying the browser UI.  
     _Recommended for faster and smoother execution._
   - **With GUI**: The Chrome browser UI will appear, and the scraping process will happen visibly.  
     _Suitable for observing the scraping process in real time._
