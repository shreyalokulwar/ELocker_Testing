# Eloader_Testing 🚀

![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?logo=github)
![CI Status](https://github.com/shrejalchoular/Eloader_Testing/actions/workflows/selenium-tests.yml/badge.svg)

This project automates testing for file upload/download functionality, file size validation, and dashboard interaction using Selenium and Python. It also includes a static front-end hosted via GitHub Pages.

---

## 🌐 Live Demo  
Visit the deployed site: [Eloader_Testing](https://shrejalchoular.github.io/Eloader_Testing/)

---

## 📁 Folder Structure

Eloader_Testing/
├── index.html              # Static front-end
├── styles.css              # Styling for the front-end
├── script.js               # JavaScript logic
├── pages/                  # Python backend modules
├── tests/                  # Selenium test scripts
├── chromedriver.exe        # Local testing driver (excluded from GitHub)
├── sample.pdf              # Sample file for upload test
├── large.pdf               # Large file for size validation
├── .gitignore              # Excludes unnecessary files
├── README.md               # Project documentation

---

## 🚀 Features

- Upload and download file testing  
- File size validation  
- Dashboard page automation  

---

## 🧪 Technologies Used

- **Frontend**: HTML, CSS, JavaScript  
- **Backend Testing**: Python, Selenium, Pytest  
- **CI/CD**: GitHub Actions  
- **Browser Automation**: Google Chrome + ChromeDriver  

---

## 📦 How to Run Tests Locally

1. Install dependencies:
   ```bash
   pip install selenium pytest
