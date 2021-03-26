web: python linkdisksappp.py runserver 0.0.0.0:$PORT

web: gunicorn linkdisksappp:app

web: waitress-serve --port=$PORT linkdisksappp:app



