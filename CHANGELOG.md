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
