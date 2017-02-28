# employee-manager

git clone https://github.com/aaronenberg/employee-manager . 
virtualenv venv
cd venv 
source bin/activate
pip install -r requirements.txt
cd MLHC 
python manage.py makemigrations
python manage.py migrate
