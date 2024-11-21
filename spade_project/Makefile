# Define paths
NOTEBOOK = "C:/Users/barba/OneDrive/Ambiente de Trabalho/MS/MS_project/spade_project/clean_data.ipynb"
SCRIPT = "./main.py"

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
