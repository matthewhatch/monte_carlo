# Monte Carlo
Motivated by the book Mathletics

Data is pulled from baseball-reference.com and cached on local csv files by year

Current Issues;
- There is some logic issues for players with common last names.

TODO:
- If a players stats page is not proceded by 01 because another player has a similar name, we need to use 02, 03, 04, etc

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
python main.py -c 100 --player 'Mike Trout' --year 2016

```
