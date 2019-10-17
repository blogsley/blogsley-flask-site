# Pugsley Lite

## Installation

1. Navigate to a directory where you keep your software projects:

        cd projects

2. Clone the repository:

        git clone https://github.com/blogsley/blogsley-flask.git
        
3. Navigate to the new directory which contains the repository.

        cd blogsley-flask

4. Create a Python 3 virtual environment called `env`:

        python3 -m venv env
        
5. Activate the environment:

        source env/bin/activate
        
6. Install required packages:

        pip install -r requirements.txt


## PostgreSql (optional)
        sudo -u postgres -i
        psql
        postgres=# createdb blogsleyflask;
        postgres-# createuser blogsleyflask;
        postgres-# alter user blogsleyflask with encrypted password 'blogsleyflask';
        postgres-# grant all privileges on database blogsleyflask to blogsleyflask;

## Development

1. Activate the virtual environment, if not already active:

        cd blogsley-flask
        source env/bin/activate
        
2. Launch the Flask application in debug mode:

        ./dev
