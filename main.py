# Import necessary elements from the application layout
from app_layout import *

# Import callback functions 
from callbacks import *


# Check if the script is being executed as the main file
if __name__ == '__main__':
    # Run the application in debug mode
    app.run_server(debug=True)
