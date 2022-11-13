
# Murls - share your social media accounts

A simple platform to share your social media accounts as a single link

Try on : https://murls.pythonanywhere.com/

Activation link at registration is disabled on pythonanywhere.

## Tech Stack
- Python
- Django
- Bootstrap 5


## Screenshots

![mockup-murls-small](https://user-images.githubusercontent.com/48137366/200274899-bc477325-36cc-4785-a946-dded52692eed.jpg)


## Run Locally

Clone the project

```bash
git clone https://github.com/arczi0/murls
```

Create virtual environment

```bash
python -m venv venv
```

For Windows use:
```bash
venv\Scripts\activate
```

Go to the project directory

```bash
cd murls
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python manage.py runserver
```

If you want use this app in local network (eg. on mobile device) edit hosts in settings.py and run:

```bash
python manage.py runserver 'YOUR-IP-ADDRESS:PORT'
```

## Roadmap

- Add custom themes
