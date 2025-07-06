install:
	pip install -r requirements.txt

run: redis-run
	uvicorn src.main:app --reload

test:
	set PYTHONPATH=. && pytest

docker:
	docker build -t tickethub .
	docker run -p 8000:8000 tickethub

docs:
	redoc-cli bundle openapi.json -o static/docs.html

redis-run:
	docker start tickethub-redis || docker run -d -p 6379:6379 --name tickethub-redis redis

redis-stop:
	docker stop tickethub-redis
