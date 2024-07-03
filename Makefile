# Define directories
HTML_FILES_DIR = html_files
MEDIA_DIR = static/media
DATA_DIR = data

# Clean target
.PHONY: clean
clean:
	@echo "Cleaning directories..."
	@rm -rf $(HTML_FILES_DIR) $(MEDIA_DIR) $(DATA_DIR)
	@echo "Directories cleaned."

# Run the Python script for parsing the website
.PHONY: parse
parse:
	@echo "Running the Python file to parse the website..."
	@python3 main.py

# Run the async parser
.PHONY: async_parse
async_parse:
	@echo "Running the async Python file to parse the website..."
	@python3 async_main.py

# Run the server
.PHONY: server
server:
	@echo "Starting the server..."
	@python3 -m http.server 8000
