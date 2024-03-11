# Monte Carlo
Motivated by the book Mathletics

Currently, this is used to calculate Runs Created for Mike Trout in 2016.

TODO:
- Calculate RC for any player from any year
- Determine where to pull stats for players

```bash
# clone
git clone git@github.com:matthewhatch/monte_carlo.git
cd monte_carlo

# create environment
python -m venv env

#activate environment and install dependencies
source env/bin/activate
pip install -r requirements.txt

# run 100 simualtions
python main.py -c 100
```
