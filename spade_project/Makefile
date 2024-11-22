# Define paths
NOTEBOOK = "./clean_data.ipynb"
SCRIPT = "./main.py"
HOST = "./plot_visualization.py"

# Default target when 'make' is called without any arguments
all: run

# Run the Jupyter notebook -- not working for now
run_notebook:
	@echo "Running the Jupyter notebook..."
	@jupyter nbconvert --to notebook --execute $(NOTEBOOK)

# Run the main Python script
run:
	@echo "Running the main Python script..."
	@python $(SCRIPT)

# Run the visualization script
run_host:
	@echo "Running the visualization script..."
	@python $(HOST)
