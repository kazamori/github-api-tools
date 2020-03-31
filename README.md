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
usage: gh-cli [-h] [--disable-cache]
              [--repository [REPOSITORIES [REPOSITORIES ...]]] [--style STYLE]
              [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --disable-cache       disable cache
  --repository [REPOSITORIES [REPOSITORIES ...]]
                        set repositories
  --style STYLE         set figure style for seaborn
  --verbose             set verbose mode
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

You can see a figure created by your-repository.csv.

![](https://github.com/kazamori/github-api-tools/raw/master/example/figures/sample-pr-stats1.png)

## Reference

* https://developer.github.com/v3/
* https://github.com/PyGithub/PyGithub
