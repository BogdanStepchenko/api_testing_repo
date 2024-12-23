# Meme API Testing

This repository contains automated tests for verifying the Meme API. The tests are grouped by key functionalities, such as retrieving all memes, fetching specific memes by ID, creating new memes, deleting memes, and validating authorization tokens.

---

## 📋 Features

### **General Features**

- Authorization checks for API access.
- Validation of response structure using Pydantic models.
- Handling of error scenarios (e.g., invalid tokens, non-existent IDs).

### **Functional Blocks**

1. **Get All Memes**:
   - Ensures all memes can be retrieved by authorized users.
   - Verifies required fields: `id`, `info`, `tags`, `text`, `updated_by`, `url`.
   - Checks for unique meme IDs.
   - Validates behavior for unauthorized users.

2. **Get a Specific Meme by ID**:
   - Ensures an authorized user can fetch a meme by ID.
   - Validates the structure and content of the response.
   - Handles scenarios for invalid IDs, deleted memes, and unauthorized access.

3. **Get Authorization Token**:
   - Validates that the token is active and functional.
   - Ensures the response contains the correct username.
   - Handles invalid or malformed tokens.

4. **Post a Meme**:
   - Ensures authorized users can create memes with valid payloads.
   - Verifies that all fields in the response match the payload.
   - Checks behavior for unauthorized users, invalid tokens, and incorrect payloads.

5. **Post New Token**:
   - Ensures valid tokens can be created with different input names.
   - Validates that duplicate names are handled correctly.
   - Checks error responses for invalid or empty names.

6. **Put Existing Meme**:
   - Ensures authorized users can update existing memes with valid payloads.
   - Validates that updated fields (`info`, `tags`, `text`, `url`) are properly modified.
   - Verifies that `id` remains unchanged and the `updated_by` field reflects the authorized user.
   - Handles error scenarios for:
     - Unauthorized users trying to update memes (401 Unauthorized).
     - Users attempting to update memes created by others (403 Forbidden).
     - Invalid tokens (401 Unauthorized).
     - Incorrect payloads (e.g., missing required fields, invalid `id`), returning a 400 Bad Request.
   - Confirms that memes cannot be updated if required fields are missing.

7. **Delete a Meme**:
   - **Authorized Deletion**: Ensures that authorized users can delete existing memes successfully.
   - **Unauthorized Deletion**: Tests that unauthorized users cannot delete memes, returning a 401 Unauthorized status.
   - **Non-Existent Meme**: Verifies that trying to delete a meme with an invalid or non-existent ID results in a 404.
   - **Re-Deletion**: Ensures that attempting to delete an already deleted meme returns a 404 Not Found status.
   - **Invalid Token**: Tests that providing an invalid token while attempting to delete a meme returns a 401 status.
   - **Ownership Check**: Ensures that users cannot delete memes that they do not own, returning a 403 Forbidden status.

## 📂 Project Structure

The project is organized into the following key directories:

### **1. `endpoints` Folder**
Contains classes responsible for handling API interactions for each test. 
These classes define the logic for performing various operations like retrieving, creating, updating, and 
deleting memes, as well as validating authorization tokens.

Some key files in this folder:
- **basic_class.py**: Contains base functionality for handling API request, such as GET, POST, PUT, and DELETE requests.
- **delete_meme.py**: Defines the functionality for deleting memes.
- **get_exact_meme.py**: Defines the functionality for getting exact meme.
- **get_token.py**: Defines the functionality for getting token.
- **post_new_meme.py**: Contains logic for posting new memes.
- **post_token.py**: Handles the creation and validation of authorization tokens.
- **put_existed_meme.py**: Defines the functionality for updating memes (PUT requests).

### **2. `tests` Folder**
This folder contains the automated test cases for verifying the functionality of the Meme API. 
The tests use `pytest` to run the test suite and generate detailed reports with `allure`.

Some key files in this folder:
- **test_delete_meme.py**: Contains tests related to deleting memes.
- **test_get_all_memes.py**: Contains tests for getting all memes.
- **test_get_exact_meme.py**: Includes tests for getting exact meme.
- **test_get_token.py**: Tests related to generating and validating authorization tokens.
- **test_post_meme.py**: Tests for posting new memes.
- **test_put_meme.py**: Contains tests for updating existing memes.
- **test_token_creation.py**: Contains tests for token creation.

### **3. `data` Folder**
Contains various payloads, constants, and utility functions used in tests.

- **constants.py**: Includes constant values such as base URLs for different API endpoints.
- **payloads_for_meme_creation.py**: Contains payloads for meme creation, including correct and incorrect variations.
- **payloads_for_meme_updation.py**: Contains functions to generate valid and invalid payloads for updating memes.
- **randomizer.py**: A helper function for generating random strings used in meme data.

### **4. `models` Folder**
This folder contains Pydantic models used for validating the structure of API responses and request data.

- **meme_data.py**: Defines the `MemeJson` model, which represents the structure of a meme's data. 
It ensures that all required fields such as `id`, `info`, `tags`, `text`, `updated_by`, and `url` are properly validated when interacting with the Meme API.

---

## 🛠 Technologies Used

- **Python 3.12**
- **pytest** — for testing.
- **allure** — for generating detailed reports.
- **requests** — for making HTTP requests.
- **GitHub Actions** — for Continuous Integration and Continuous Deployment (CI/CD).

---

## 🚀 Running the Tests with CI/CD

The tests are automatically run via GitHub Actions, as defined in the `.github/workflows/run_test.yml` file. The workflow allows you to trigger the tests manually, selecting the severity of the tests to run.

### Triggering the Tests:

1. Go to the **Actions** tab in the GitHub repository.
2. Select the workflow called **Run autotest**.
3. Click on **Run workflow** on the right side of the screen.
4. Choose the test severity from the dropdown options:
   - **all**: Runs all tests.
   - **fast_smoke**: Runs a quick smoke test suite.
   - **smoke**: Runs a full smoke test suite.
   - **full_test**: Runs all tests in full mode.
5. The selected tests will be executed automatically in the GitHub Actions environment.

### After the tests run:
- The results will be available as artifacts and can be accessed directly from the GitHub Actions interface.
- Detailed test reports will be generated with Allure and uploaded to GitHub Pages, allowing you to view the test results through a browser.

---

With this CI/CD setup, you can easily run and track your tests without needing to manually trigger them on your local machine, ensuring that your Meme API remains robust and functional.
