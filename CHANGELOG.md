# 0.3.3 (2023-11-05)

-  Refactored `respond` method in `serf` class to enforce payload type as bytes.

# 0.3.2 (2023-11-05)

-  Payload in serf queries has been made optional and related tests have been updated.

# 0.3.1 (2023-11-05)

-  Added `query_one` method in `serf` module and its corresponding test in `test_serfio`.

# 0.3.0 (2023-11-05)

-  Simplified the `Serf` class methods.
-  Enhanced error handling.
-  Updated tests to reflect changes in error handling.
-  Commented out several methods in the `Serf` class.

# 0.2.6 (2023-11-05)

-  Added type checking for `filter_nodes` and `filter_tags`.

# 0.2.5 (2023-11-01)

-  Refactored task cancellation in protocol to handle asyncio errors.

# 0.2.4 (2023-11-01)

-  Added tests for `respond` and `query` methods
-  Added tests for `auth` method

# 0.2.3 (2023-11-01)

-  Transitioned from `pycodestyle` to `flake8` for linting.
-  Reformatted code for improved readability.
-  Integrated `isort` and `black` into the pre-commit, makefile, and `pipfile`.
-  Updated GitHub Actions workflow to include testing with `pytest` on Python 3.11 and Docker setup.

# 0.2.2 (2023-11-01)

-  Enhanced testing capabilities with the addition of pytest coverage.
-  Introduced error handling to the protocol's _recv method.
-  Introduced debug logging in protocol and serf modules.

# 0.2.1 (2023-11-01)

-  Added `pre-commit`, configured hooks, and updated pipfile dependencies.

# 0.2.0 (2023-11-01)

-  **Testing Environment Improvements**: Added pytest. Introduced a pytest fixture for serf server with Docker integration.
-  **Serf Connection Logic Refactoring**: Refactored Serf connection logic and added async context management to the serf class.

# 0.1.0 (2023-10-31)

-  Initial release.
