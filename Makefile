run:
	uv run lowest_price_service.py

graph:
	uv run graph.py

rungraph:
	uv run lowest_price_service.py && uv run graph.py
