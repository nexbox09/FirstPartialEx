# Telecom Analysis Project

This project analyzes telecommunications data for Mexico using both Octave and Python. Below are instructions for setting up and running the code, as well as online alternatives if you prefer not to install software locally.

## Octave Instructions

### Local Installation

1. Download and install Octave from the [official website](https://www.gnu.org/software/octave/download.html).
2. Clone or download this repository to your local machine.
3. Open Octave and navigate to the project directory.
4. Run the script by typing the name of the .m file (without the extension) in the Octave command window. For example:
   ```
   octave> telecom_analysis
   ```

### Online Alternative

If you prefer not to install Octave locally, you can use Octave Online:

1. Go to [Octave Online](https://octave-online.net/).
2. Copy and paste the contents of the .m file into the editor.
3. Click "Run" to execute the code.

## Python Instructions

### Local Installation

1. Install Python from the [official website](https://www.python.org/downloads/).
2. Clone or download this repository to your local machine.
3. Navigate to the project directory in your terminal or command prompt.
4. It's recommended to create a virtual environment:
   ```
   python -m venv venv
   ```
5. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
6. Install the required packages using the requirements.txt file:
   ```
   pip install -r requirements.txt
   ```
7. Run the script using:
   ```
   python app.py
   ```

### Online Alternatives

1. Google Colab:
   - Go to [Google Colab](https://colab.research.google.com/).
   - Create a new notebook.
   - Copy and paste the Python code into a cell.
   - Upload the CSV data file to the Colab environment.
   - Adjust the file path in the code to match the uploaded file location.
   - Run the cell to execute the code.

2. Jupyter Notebook via Binder:
   - Create a GitHub repository with your Python script and a `requirements.txt` file listing the necessary packages.
   - Go to [Binder](https://mybinder.org/) and enter your GitHub repository URL.
   - Click "Launch" to create a Jupyter Notebook environment with your code and dependencies.

## Data

Ensure that your data file (CSV format) is in the same directory as your script, or adjust the file path in the code accordingly.

## Output

The scripts will generate various plots and statistical analyses based on the telecommunications data. Check the console output for any additional information or results.

For any issues or questions, please open an issue in this repository.
