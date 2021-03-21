import typer
from itertools import combinations

app = typer.Typer()

def split(number, sep):
    typer.echo(number)
    n = len(number)
    for k in range(1, n):
        for combination in combinations(range(n-1), k):
            new_number = []
            begin = 0
            for position in combination:
                new_number.append(number[begin:position+1])
                begin = position + 1
            new_number.append(number[position+1:])
            typer.echo(sep.join(new_number))

            " ".join

@app.command()
def main(number: str, sep: str = " "):
    split(number, sep)

if __name__ == "__main__":
    app()
