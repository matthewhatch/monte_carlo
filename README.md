# Monte Carlo
Generate Runs Created(RC) for any player, in any year in Major Leage Baseball
Motivated by the book Mathletics

Data is pulled from baseball-reference.com and cached on local csv files by year


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
