# github-api-tools

CLI tools for GitHub API

## How to install

```bash
$ git clone git@github.com:kazamori/github-api-tools.git
$ cd github-api-tools
$ python setup.py develop
```

Confirm `gh-cli` command show help.

```bash
$ gh-cli --help
usage: gh-cli [-h] [--disable-cache] [--nop]
              [--repository [REPOSITORIES [REPOSITORIES ...]]] [--verbose]
              [--version] [--palette PALETTE] [--style STYLE]
              {box,scatter} ...

positional arguments:
  {box,scatter,violin}

optional arguments:
  -h, --help            show this help message and exit
  --disable-cache       disable cache
  --nop                 use as a separator for option handling of positional
                        argument
  --repository [REPOSITORIES [REPOSITORIES ...]]
                        set repositories
  --verbose             set verbose mode
  --version             show version
  --palette PALETTE     set palette parameter for seaborn plot
  --style STYLE         set style parameter for seaborn plot
```

## How to run

Set Personal access tokens. You can get from https://github.com/settings/tokens .

```bash
$ export GITHUB_API_TOKEN="********"
```

Run `gh-cli` command.

```bash
(github-api) $ gh-cli --repository organization/your-repository
2020-03-28 21:21:44,479 INFO Repository: your-repository
2020-03-28 21:21:44,479 INFO           : https://github.com/organization/repo.git
2020-03-28 21:21:45,862 INFO #61: Xxx
2020-03-28 21:21:47,437 INFO #60: Yyy
2020-03-28 21:21:48,957 INFO #59: Zzz
...
```

`gh-cli` creates a CSV file about Pull Requests created by yourself.

[vviewer](https://github.com/t2y/vviewer) show values with columns every one line vertically. It's useful to check data.

```bash
$ vviewer your-repository.csv
...
------------------------------------------------------------------------
001: additions                    : 467
002: changed_files                : 32
003: changes                      : 266
004: closed_at                    : 2020-03-27 07:06:34
005: comments                     : 6
006: created_at                   : 2020-03-25 06:53:42
007: deletions                    : 201
008: elapsed_days                 : 2.008935185185185
009: elapsed_days_of_first_comment: 1.7815972222222223
010: html_url                     : https://github.com/organization/your-repository/pull/60
011: labels_                      : refactoring
012: merged                       : True
013: number                       : 60
014: reviews                      : other-user
015: title                        : Refactor something
016: user.login                   : t2y
------------------------------------------------------------------------
```

### Scatter plot

You can see a scatter plot created by your-repository.csv by default.

![](https://github.com/kazamori/github-api-tools/raw/master/example/figures/sample-scatter-pr-stats1.png)

`scatter` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli scatter --help
usage: gh-cli scatter [-h] [--alpha ALPHA] [--col COL] [--col_wrap COL_WRAP]
                      [--height HEIGHT]

optional arguments:
  -h, --help           show this help message and exit
  --alpha ALPHA        set alpha parameter for relplot
  --col COL            set col parameter for relplot
  --col_wrap COL_WRAP  set col_wrap parameter for relplot
  --height HEIGHT      set height parameter for seaborn plot
```

### Box plot

![](https://github.com/kazamori/github-api-tools/raw/master/example/figures/sample-box-pr-stats1.png)

`box` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli box --help
usage: gh-cli box [-h] [--height HEIGHT] [--width WIDTH]

optional arguments:
  -h, --help       show this help message and exit
  --height HEIGHT  set height parameter for subplots
  --width WIDTH    set width parameter for subplots
```

### Violin plot

![](https://github.com/kazamori/github-api-tools/raw/master/example/figures/sample-violin-pr-stats1.png)

`violin` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli violin --help
usage: gh-cli violin [-h] [--height HEIGHT] [--inner INNER] [--loc LOC]
                     [--width WIDTH]

optional arguments:
  -h, --help       show this help message and exit
  --height HEIGHT  set height parameter for subplots
  --inner INNER    set inner parameter for violinplot
  --loc LOC        set loc parameter for legend
  --width WIDTH    set width parameter for subplots
```

## Reference

* https://developer.github.com/v3/
* https://github.com/PyGithub/PyGithub
