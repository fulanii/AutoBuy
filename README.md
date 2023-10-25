# AutoBuy
Is a Python-based automation & testing project focused on interacting with Ecommerce websites. The project employs Selenium, to automate various tasks, including user login, session management etc. It is structured as a Python package with modules to maintain code clarity, and different aspects of the automation and testing process.


Project goal: The goal of this project is to showcase web testing and automation skills. The GitHub repository serves as a central location for code management, collaboration and showcase.


## Project Structure
```markdown
AutoBuy/
|   docs/
│   |   ├─ ...
|   examples/
│   |   ├─ ...
|   .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── home_depot/
|   │   │   ├── __init__.py
|   │   │   ├── logins/
|   │   │   │   └── __init__.py
|   │   │   │   └── fresh_login.py
|   |   │   │   └── cookies_login.py
|   |   │   │   └── logout.py
│   ├── utils/
│   │   └── __init__.py
│   │   └── webdriver_path.py
│   │   └── driver_manager.py
|   |   ├── custom_exceptions/
|   |   |   └── __init__.py
|   |   |   └── exceptions.py
│   ├── tests/
│   │   └── __init__.py
│   │   └── test_home_depot/
│   │   |   └── __init__.py
│   │   |   └── test_login.py
│   └── config/
│   │   └── __init__.py
│   │   └── config.py
│   │   └── config.ini
├── README.md
├── requirements.txt
└── setup.py
|__ .gitignore
```

<!-- 
## Tech Stack:
Programming Language: Python 3.11.x

Python Libraries:
- Selenium 4.9: Web automation framework for web scraping and interaction.
- Py-test 7.4 and Unittest: for assertion and unit tests

Web Automation:
- Chrome WebDriver 117: Selenium WebDriver for controlling Chrome browser.
- Chrome v117 DevTools: Utilized for inspecting and debugging web pages.

Version Control and Collaboration:
- Git
- GitHub
- act

Continuous Integration:
- GitHub Actions: For automating workflows and tasks, such as testing and deployment.

Data Storage:
- Serialization: Storing session data and state for user interactions on the Home Depot website.

Web Technologies:
- HTML5
- CSS3


##  -->