restart_doc:
	docker compose down
	docker rmi -f exam_bot-bot
	docker compose up