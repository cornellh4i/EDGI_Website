# EDGI_Website
EDGI (Environmental Data Governance Initiative) is a non-profit organization that aims to find trends in regard to Environmental Protection Agency (EPA) work. Specifically, EDGI works to identify ways the EPA neglects various communities throughout the USA.
## About the Project 
The project aims to develop an interactable, user-friendly website platform that displays the data analytics and visualizations. 
### Built With 
[Streamlit](https://streamlit.io/)
[Folium](https://folium.streamlit.app/)


### Installation 
1. Clone the repo <br/> `git clone https://github.com/cornellh4i/EDGI_Website.git`
2. Set up virtual environment <br/> `pip install virtualenv` 
3. Create a virtual environment. Replace `env_name` with your desired environment name:
        `python -m virtualenv env_name`
4. Activate the virtual environment: <br/>
    Windows: `env_name/Scripts/activate` <br/>
    macOS and Linux: `source env_name/bin/activate`

5. `pip install -r requirements.txt` to install dependencies
6. Navigate to frontend folder and run `streamlit run main.py` to open in default web browser
7. Handling potential errors:
- The ECHO_modules in the frontend folder sometimes will be overwritten and become empty. Navigate to the ECHO_modules/ECHO_modules in backend and copy the inner ECHO_modules folder into frontend, rerun the script, and it should run fine.
- There is a small error in the Region.py code on line 5. Instead of "from AllPrograms_util import get_region_rowid", it should be "from .AllPrograms_util import get_region_rowid"
### Github Process
1. Assign tickets to pairs --> make a new branch
2. Dev pairs finish their work within their branch and make a PR(pull request) 
3. Tech leads will review the PR, make comments to the code
4. Dev pairs will improve their code and iterate this process 
5. Tech leads will merge the PR to the main branch(and resolve any potential conflicts)
