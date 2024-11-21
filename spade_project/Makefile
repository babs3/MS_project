# Define paths
DATASET_DIR = "./datasets"
NOTEBOOK = "C:/Users/barba/OneDrive/Ambiente de Trabalho/MS/MS_project/spade_project/clean_data.ipynb"
SCRIPT = "./main.py"

# Clean the datasets directory
clean:
	@echo "Cleaning datasets folder..."
	@del /Q $(DATASET_DIR)\*     # Removes all files in the dataset folder
	@for /d %%i in ($(DATASET_DIR)\*) do rmdir /s /q %%i  # Removes subdirectories

# Default target when 'make' is called without any arguments
all: run

# Run the Jupyter notebook
run_notebook:
	@echo "Running the Jupyter notebook..."
	@jupyter nbconvert --to notebook --execute $(NOTEBOOK)

# Run the main Python script
run:
	@echo "Running the main Python script..."
	@python $(SCRIPT)
