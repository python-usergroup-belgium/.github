# GitHub profile

Dynamic GitHub profile - GitHub actions (CICD) updates the `README.md` daily.

Built with:

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [cogapp](https://nedbatchelder.com/code/cog)
- [python-dateutil](https://dateutil.readthedocs.io/en/stable/)
- [loguru](https://loguru.readthedocs.io/en/stable/index.html)

## Get started

1. Make sure you have Python 3.11 installed
   1. I.e.: `pyenv install 3.11.0 && pyenv local 3.11`
2. Clone the repo: `git clone git@github.com:python-usergroup-belgium/.github.git`
3. Create a new virtual environment: `python -m venv .venv`
4. Activate the environment
   1. I.e.: `source .venv/bin/activate`
3. Install the dependencies: `pip install ".[qa]"`
4. Install pre-commit hooks `pre-commit install`

Dynamic information is defined by `utils/`, ran daily via GitHub actions (CICD)
(`.github/workflows/update-readme.yaml`). Static information is already on `profile/README.md`.
