set -eux pipefail

# Clean out the directories first
rm -rf ./lib
rm lambda_function.zip

# Install the dependencies then zip it up.
pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py