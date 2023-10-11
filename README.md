# GitHub Pull Requests Summary Script

This script fetches a summary of open, closed, and draft pull requests from the past week for a specified GitHub repository.

### Prerequisites

- Python 3+

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/danpaldev/repositoryname.git
   ```

2. Create a virtual environment and activate it:

   **On macOS and Linux:**

   ```shell
   python3 -m venv env
   source env/bin/activate
   ```

   **On Windows:**

   ```shell
   py -m venv env
   .\env\Scripts\activate
   ```

3. Install the required packages:

   ```shell
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of the project, and add the following variables with the actual username of the repository owner and the repository name:

   ```shell
   REPO_OWNER=
   REPO_NAME=
   ```

## Usage

After setting up the repository owner and repository name in the .env file, simply run the script:

```shell
python pr_script.py
```

The program fetches a list of pull requests and prints a summary to the console.
